import datetime as dt
import json
import string
import time
from typing import Optional, Dict, Union, List

import lumipy.provider as lp
import numpy as np
import pandas as pd
from lumipy.provider import ColumnMeta, ParamMeta
from lumipy.provider.metadata import TableParam
from lumipy.query.expression.sql_value_type import SqlValType
from pandas import DataFrame
from pytz import utc


class ParameterAndLimitTestProvider(lp.BaseProvider):

    def __init__(self):
        columns = [
            ColumnMeta('Name', SqlValType.Text),
            ColumnMeta('StrValue', SqlValType.Text),
            ColumnMeta('Type', SqlValType.Text),
        ]
        params = [
            ParamMeta('Param1', data_type=SqlValType.Int, default_value=0),
            ParamMeta('Param2', data_type=SqlValType.Text, default_value='ABC'),
            ParamMeta('Param3', data_type=SqlValType.Double, default_value=3.1415),
            ParamMeta('Param4', data_type=SqlValType.Date, default_value=dt.datetime(2022, 1, 1, 13, 15, 2)),
            ParamMeta('Param5', data_type=SqlValType.DateTime, is_required=True),
            ParamMeta('Param6', data_type=SqlValType.Boolean, default_value=False),
        ]
        super().__init__('test.pyprovider.paramsandlimit', columns=columns, parameters=params)

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:
        rows = [
            {
                'Name': k,
                'StrValue': str(v),
                'Type': type(v).__name__,
            }
            for k, v in params.items()
        ]
        rows.append({'Name': 'limit', 'StrValue': str(limit), 'Type': type(limit).__name__})

        return pd.DataFrame(rows)


class TableParameterTestProvider(lp.BaseProvider):

    def __init__(self):
        columns = [
            ColumnMeta('TableVarColName', SqlValType.Text),
            ColumnMeta('TableVarColType', SqlValType.Text),
            ColumnMeta('TableVarNumCols', SqlValType.Int),
            ColumnMeta('TableVarNumRows', SqlValType.Int),
        ]
        table_params = [
            TableParam('TestTable')
        ]
        super().__init__('test.pyprovider.tablevar', columns=columns, table_parameters=table_params)

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:
        df = params['TestTable']

        return pd.DataFrame(
            {
                'TableVarColName': n,
                'TableVarColType': t.name,
                'TableVarNumCols': df.shape[1],
                'TableVarNumRows': df.shape[0],
            }
            for n, t in df.dtypes.items()
        )


class PandasFilteringTestProvider(lp.PandasProvider):

    def __init__(self, seed):

        np.random.seed(seed)

        test_value_fns = [
            lambda: np.random.randint(1, 100),
            lambda: np.random.normal(-10, 5),
            lambda: ''.join(
                np.random.choice(list(string.printable[:-3]), replace=True, size=np.random.randint(50, 250))
            ) if np.random.binomial(1, 0.9) else None,
            lambda: dt.datetime(2022, 1, 1, tzinfo=utc) + dt.timedelta(days=np.random.randint(-100, 100)),
            lambda: bool(np.random.binomial(1, 0.5)),
        ]

        df = pd.DataFrame(
            {f"Col_{k}": test_value_fns[i % len(test_value_fns)]() for i, k in enumerate("ABCDEFGH")}
            for _ in range(10000)
        )

        super().__init__(df, name='Test.Filtering')
        self.columns['FilterString'] = ColumnMeta('FilterString', SqlValType.Text)

    def get_data(
            self,
            data_filter: Dict[str, Union[List, Dict]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        df = super().get_data(data_filter, limit, **params)
        df['FilterString'] = json.dumps(data_filter)
        return df


class FilteringTestProvider(lp.BaseProvider):

    def __init__(self):

        super().__init__(
            'test.pyprovider.filter',
            columns=[
                ColumnMeta('NodeId', SqlValType.Int),
                ColumnMeta('OpName', SqlValType.Text),
                ColumnMeta('Input', SqlValType.Text),
            ]
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        flattened = []

        def flatten(fobj):

            op_name, op_args = fobj['OP'], fobj['EX']
            flattened.append({
                'OpName': op_name,
                'Input': json.dumps(op_args)
            })

            if op_name.endswith('Value'):
                return
            else:
                [flatten(op_arg) for op_arg in op_args]

        flatten(data_filter)

        return pd.DataFrame({**{'NodeId': i}, **d} for i, d in enumerate(flattened))


class ColumnValidationTestProvider(lp.BaseProvider):

    def __init__(self):

        columns = [ColumnMeta(f'Col{i}', SqlValType.Int) for i in range(5)]
        params = [ParamMeta('HasBadCols', SqlValType.Boolean, default_value=False)]

        super().__init__(
            'test.pyprovider.dataframe.validation',
            columns=columns,
            parameters=params,
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        if params.get('HasBadCols'):
            # Test that it will throw if the column sets don't match.
            return pd.DataFrame(
                {f'Col{i}': np.random.randint(100) for i in range(3, -1, -1)}
                for _ in range(100)
            )
        else:
            # Test that it's ok if the column names are out of order but the sets match
            return pd.DataFrame(
                {f'Col{i}': np.random.randint(100) for i in range(4, -1, -1)}
                for _ in range(100)
            )


class TaskCancelledTestProvider(lp.BaseProvider):

    def __init__(self):
        super().__init__(
            'test.waits.forever',
            columns=[ColumnMeta('TestCol', SqlValType.Text)],
            parameters=[ParamMeta('WaitTime', SqlValType.Int, default_value=600)]
        )

    def get_data(
            self,
            data_filter: Optional[Dict[str, object]],
            limit: Union[int, None],
            **params
    ) -> DataFrame:

        time.sleep(params.get('WaitTime'))
        return pd.DataFrame({'TestCol': list('abcdefg')})
