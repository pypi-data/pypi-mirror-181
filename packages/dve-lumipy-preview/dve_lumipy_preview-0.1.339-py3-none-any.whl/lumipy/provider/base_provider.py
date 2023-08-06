import datetime as dt
import json
import re
import sys
import traceback
from abc import ABC, abstractmethod
from distutils.util import strtobool
from enum import Enum
from math import ceil
from typing import List, Optional, Dict, Union, Any, Type

import pandas as pd
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pandas import DataFrame

from lumipy.common.string_utils import indent_str
from lumipy.provider.translation import table_dict_to_df
from lumipy.provider.metadata import (
    ColumnMeta, ParamMeta, TableParam,
    RegistrationType, RegistrationCategory, RegistrationAttributes, LifeCycleStage
)
from lumipy.query.expression.sql_value_type import SqlValType
from collections.abc import Iterable

CHUNK_SIZE = 10000


def _cast(name: str, value: Any, data_type: str) -> Union[int, float, str, bool, DataFrame, dt.datetime, None]:
    data_type = SqlValType[data_type]

    if value is None:
        return value

    if data_type == SqlValType.Int:
        return int(value)
    elif data_type == SqlValType.Double:
        return float(value)
    elif data_type == SqlValType.Text:
        return str(value)
    elif data_type == SqlValType.Boolean:
        return bool(strtobool(str(value)))
    elif data_type == SqlValType.Table:
        return table_dict_to_df(value)
    elif data_type == SqlValType.DateTime:
        return pd.to_datetime(value, utc=True)
    elif data_type == SqlValType.Date:
        return pd.to_datetime(value, utc=True)
    else:
        TypeError(f"Unsupported data type for parameter '{name}': {data_type.name}.")


def _metadata_type_check(name: str, target_type: Type, values: Union[str, Enum, Iterable]):
    if not hasattr(values, '__len__'):
        values = [values]

    if len(values) == 1 and values[0] is None:
        return

    for value in values:
        if value is not None and not isinstance(value, target_type):
            raise TypeError(f"{name} input value must be type {target_type.__name__} but was {type(value).__name__}.")


class BaseProvider(ABC):
    """Abstract base class for local python luminesce providers.

    All local provider classes must inherit from this class, call super().__init__() and implement the _get_data method.

    """

    @abstractmethod
    def __init__(
            self,
            name: str,
            columns: List[ColumnMeta],
            parameters: Optional[List[ParamMeta]] = None,
            table_parameters: Optional[List[TableParam]] = None,
            description: Optional[str] = None,
            documentation_link: Optional[str] = None,
            license_code: Optional[str] = None,
            registration_category: Optional[RegistrationCategory] = RegistrationCategory.OtherData,
            registration_attributes: Optional[RegistrationAttributes] = RegistrationAttributes.none,
            lifecycle_stage: Optional[LifeCycleStage] = LifeCycleStage.Experimental,
    ):
        """Constructor of the BaseProvider class.

        Args:
            name (str): name to give the provider (e.g. Example.Local.Provider).
            columns (List[ColumnMeta]): list of columns metadata objects that define the parameter's columns.
            parameters (Optional[List[ParamMeta]]): optional list of parameter metadata objects that define the
            provider's parameters. If no values are supplied then the provider will be parameterless.
            description (Optional[str]): description of the provider.
            documentation_link (Optional[str]): the url linking to the provider documentation.
            license_code (Optional[str]): the license code of this provider.
            registration_category (Optional[RegistrationCategory]): registration category of the provider.
            registration_attributes (Optional[RegistrationAttributes]): registration attributes of the provider.
            lifecycle_stage (Optional[LifeCycleStage]): stage of the development lifecycle of the provider.

        """

        if (name is None) or re.match('^[a-zA-Z0-9.]+$', name) is None:
            raise ValueError("Provider name must be a non-empty string containing only '.' and alphanumeric chars. "
                             f"Was {name}")

        if (len(columns) == 0) or any(not isinstance(c, ColumnMeta) for c in columns):
            raise TypeError(f"Provider columns input must be a non-empty list of {ColumnMeta.__name__}.")

        _metadata_type_check('parameters', ParamMeta, parameters)
        _metadata_type_check('table_parameters', TableParam, table_parameters)
        _metadata_type_check('registration_category', RegistrationCategory, registration_category)
        _metadata_type_check('registration_attributes', RegistrationAttributes, registration_attributes)
        _metadata_type_check('lifecycle_stage', LifeCycleStage, lifecycle_stage)

        self.name = name
        self.description = description
        self.documentation_link = documentation_link
        self.license_code = license_code
        self.registration_type = RegistrationType.DataProvider
        self.registration_category = registration_category
        self.registration_attributes = registration_attributes
        self.lifecycle_stage = lifecycle_stage

        self.path_name = name.replace('.', '-').lower()

        self.columns = {c.name: c for c in columns}
        self.parameters = {p.name: p for p in parameters} if parameters is not None else {}
        self.table_parameters = {p.name: p for p in table_parameters} if table_parameters is not None else {}

    def shutdown(self) -> None:
        """Method that is called whenever the provider needs to be shut down. By default, this is a no-op, but if your
        provider needs to clean up after itself it should do it by overloading this method.

        """
        pass

    @abstractmethod
    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:
        """Abstract method that represents getting and then returning data from the provider given a data filter
        dictionary, an optional limit value, and a set of named parameter values. Overriding this method implements the
        core behaviour of the provider when its associated /api/v1/provider-name/data/ endpoint is called.

        Args:
            data_filter (Optional[Dict[str, object]]): data filter dictionary that represents a nested set of filter
            expressions on the provider data or None (no filter given in query). Inheritors must be able to handle both.
            limit (Optional[int]): integer limit value or None (no limit). Inheritors must be able to handle both.
            **params: parameter name-value pairs corresponding to the parameters given to the provider.

        Returns:
            List[Dict[str, Union[str, int, float]]]: list of dictionaries where the keys are the column names and the
            values are the column values. Each dictionary represents a row of data from the provider.
        """
        raise NotImplementedError("super()._get_data() does not do anything and shouldn't be called.")

    def _fill_defaults(self, pvs):

        pv_dict = {pv['name']: pv for pv in pvs}

        for p_name, p_meta in self.parameters.items():
            if p_name not in pv_dict.keys():
                if p_meta.default_value is None and p_meta.is_required:
                    raise ValueError(f'The parameter {p_name} of {self.name} was not given but is required.')

                pv_dict[p_name] = {'name': p_name, 'value': p_meta.default_value, 'data_type': p_meta.data_type.name}

        for tp_name in self.table_parameters.keys():
            if tp_name not in pv_dict.keys():
                raise ValueError(f'The table parameter {tp_name} of {self.name} was not given but is required.')

        return pv_dict.values()

    def validate_df(self, df: DataFrame) -> DataFrame:
        # Assert that it's a dataframe
        if not isinstance(df, DataFrame):
            raise TypeError(
                f'get_data in {self.name} did not return or yield a pandas dataframe '
                f'(iterable element was an instance of {type(df).__name__})'
            )

        # Assert that the column names are correct
        if set(df.columns) != set(self.columns.keys()):
            exp_col_str = ', '.join(sorted(list(c for c in self.columns.keys())))
            obs_col_str = ', '.join(sorted(list(df.columns)))
            raise ValueError(
                f'The column content of output from {type(self).__name__}.get_data() does not match the provider spec.\n'
                f'  Expected: {exp_col_str}\n'
                f'    Actual: {obs_col_str}'
            )

        # Arrange columns to match the order set in the ctor
        return df[list(self.columns.keys())]

    def router(self) -> APIRouter:
        """Create a FastAPI APIRouter object that implements a chunk of the API for this local provider instance.

        Returns:
            APIRouter: FastAPI APIRouter object representing the API routes for this instance.
        """

        router = APIRouter(tags=[self.name])

        @router.get(f'/api/v1/{self.path_name}/metadata')
        async def provider_metadata():
            return {
                "Name": self.name,
                "Description": self.description,
                "DocumentationLink": self.documentation_link,
                'LicenseCode': self.license_code,
                'RegistrationType': self.registration_type.name,
                'RegistrationCategory': self.registration_category.name,
                'RegistrationAttributes': self.registration_attributes.name,
                'LifecycleStage': self.lifecycle_stage.name if self.lifecycle_stage else None,
                "Columns": [c.to_dict() for c in self.columns.values()],
                "Params": [p.to_dict() for p in self.parameters.values()],
                "TableParams": [t.to_dict() for t in self.table_parameters.values()],
            }

        @router.post(f'/api/v1/{self.path_name}/data')
        async def provider_data(request: Request):

            d = await request.json()

            try:
                pvs = d.get('params')
                pvs = self._fill_defaults(pvs if pvs else [])
                param_dict = {pv['name']: _cast(**pv) for pv in pvs}

                data = self.get_data(d.get('filter'), d.get('limit'), **param_dict)

                if isinstance(data, pd.DataFrame):
                    data = [data]
                elif not isinstance(data, Iterable):
                    raise TypeError(
                        f'get_data in {self.name} did not return or yield a pandas dataframe '
                        f'(was an instance of {type(data).__name__})'
                    )

                def csv_chunks():
                    for df in data:
                        df = self.validate_df(df)
                        n_chunks = ceil(df.shape[0] / CHUNK_SIZE)
                        for i in range(n_chunks):
                            chunk = df.iloc[i * CHUNK_SIZE: (i + 1) * CHUNK_SIZE]
                            yield chunk.to_csv(index=False, header=False, na_rep='NULL')

                return StreamingResponse(csv_chunks())

            except Exception as e:
                # Package up error and return info as a 400
                err_data = {
                    "Provider": self.name,
                    "ErrorType": type(e).__name__,
                    "ErrorInfo": ''.join(traceback.format_exception(*sys.exc_info()))
                }

                print(f"\nError raised in {self.name}")
                print(indent_str(err_data["ErrorInfo"], n=4), end='\n\n')

                raise HTTPException(detail=json.dumps(err_data), status_code=400)

        return router
