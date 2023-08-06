from distutils.util import strtobool
from typing import Dict, List, Any
from typing import Union

import pandas as pd
from pandas import DataFrame, merge, Series, isna, to_datetime

from lumipy.typing.sql_value_type import SqlValType


_REGEX_ESCAPES = {
    '\\?': 'xxxQUESTIONxxx',
    '\\*': 'xxxSTARxxx',
    '\\_': 'xxxUNDERSCORExxx',
    '\\%': 'xxxPERCENTxxx',
    ' ': 'xxxSPACExxx',
    '\n': 'xxxNEWLINExxx',
    '.': 'xxxDOTxxx',
    '-': 'xxxHYPHENxxx',
    '\\': 'xxxBACKSLASHxxx',
    '|': 'xxxBARxxx',
    '^': 'xxxCARETxxx',
    '$': 'xxxDOLLARxxx',
    '=': 'xxxEQUALSxxx',
    '!': 'xxxEXCLAIMATIONxxx',
    '<': 'xxxLESSTHANxxx',
    '>': 'xxxGREATERTHANxxx',
    ':': 'xxxCOLONxxx',
    '+': 'xxxPLUSxxx',
    '{': 'xxxCURLYLEFTxxx',
    '}': 'xxxCURLYRIGHTxxx',
    '[': 'xxxSQUARELEFTxxx',
    ']': 'xxxSQUARERIGHTxxx',
    '(': 'xxxROUNDLEFTxxx',
    ')': 'xxxROUNDRIGHTxxx',
}


_OP_MAP = {
    'Not': lambda x: ~x,
    'IsNull': lambda x: isna(x),
    'IsNotNull': lambda x: ~isna(x),
    'And': lambda x, y: x & y,
    'Or': lambda x, y: x | y,
    'Gt': lambda x, y: x > y,
    'Lt': lambda x, y: x < y,
    'Gte': lambda x, y: x >= y,
    'Lte': lambda x, y: x <= y,
    'In': lambda x, y: x.isin(y),
    'NotIn': lambda x, y: ~x.isin(y),
    'Eq': lambda x, y: x == y,
    'Neq': lambda x, y: x != y,
    'Add': lambda x, y: x + y,
    'Subtract': lambda x, y: x - y,
    'Divide': lambda x, y: x / y,
    'Multiply': lambda x, y: x * y,
    'Between': lambda x, a, b: x.between(a, b, inclusive='both'),
    'NotBetween': lambda x, a, b: ~(x.between(a, b, inclusive='both')),
    'DateValue': lambda x: to_datetime(x, utc=True),
    'BoolValue': lambda x: bool(x),
    'StrValue': lambda x: str(x),
    'NumValue': lambda x: float(x),
    'ListValue': lambda *xs: [x for x in xs],
    'Mod': lambda x, m: x % m,
    'Concatenate': lambda x, y: x + y,
    'Like': lambda x, p: _like(x, p),
    'Glob': lambda x, p: _glob(x, p),
    'Regexp': lambda x, p: _regexp(x, p),
    'NotLike': lambda x, p: ~_like(x, p),
    'NotGlob': lambda x, p: ~_glob(x, p),
    'NotRegexp': lambda x, p: ~_regexp(x, p),
    'Round': lambda x, d: round(x, int(d)),
}


_LEAVES = ['ColValue', 'DateValue', 'BoolValue', 'StrValue', 'NumValue']


_BOOLEAN_FNS = [
    'And', 'Or',
    'Gt', 'Lt', 'Gte', 'Lte',
    'Eq', 'Neq',
    'In', 'NotIn',
    'Between', 'NotBetween',
    'Like', 'NotLike', 'Glob', 'NotGlob',
    'Regexp', 'NotRegexp',
]


def _apply_as_regex(char_wildcard, anylen_wildcard, case, series, pattern):
    for k, v in _REGEX_ESCAPES.items():
        pattern = pattern.replace(k, v)

    pattern = pattern.replace(char_wildcard, '(.|\\n)').replace(anylen_wildcard, '(.|\\n)*')

    for k, v in _REGEX_ESCAPES.items():
        pattern = pattern.replace(v, f'\\{k}')

    return series.str.fullmatch(pattern, na=False, case=case)


def _glob(series, pattern):
    return _apply_as_regex('?', '*', True, series, pattern)


def _like(series, pattern):
    return _apply_as_regex('_', '%', False, series, pattern)


def _regexp(series, pattern):
    pattern = pattern if pattern.startswith('^') else '.*' + pattern
    return series.str.match(pattern, na=False, case=True)


def _restriction_table(df, restriction_dict: Dict[str, List[Any]]):
    # Parse restriction table into a dataframe and then build a filter for which columns pass
    res_df = table_dict_to_df(restriction_dict)
    on_cols = res_df.columns.tolist()
    merge_df = merge(df, res_df, how='left', on=on_cols, indicator=True)
    return merge_df['_merge'] == 'both'


def _col_value(df, x):
    # If column isn't present, return None for partial filter application
    return df[x] if x in df.columns else None


def apply_filter(df: DataFrame, data_filter: Union[None, Dict[str, object]]) -> DataFrame:
    """Apply a data filter to a pandas DataFrame

    Args:
        df (DataFrame): the dataframe to apply the filter to.
        data_filter (Union[None, Dict[str, object]]): the data filter to apply. If it's none then this function is a
        no-op.

    Returns:
        DataFrame: the filtered dataframe.

    """

    if data_filter is None:
        return df

    def translate(fobj: Dict[str, Union[Dict, List, object]]) -> Union[Series, None, float, str, bool]:

        op_name, op_args = fobj['OP'], fobj['EX']

        if not isinstance(op_args, list):
            op_args = [op_args]

        if op_name == 'ColValue':
            fn = lambda x: _col_value(df, x)
        elif op_name == 'RestrictionTable':
            fn = lambda x: _restriction_table(df, x)
        elif op_name in _OP_MAP.keys():
            fn = _OP_MAP[op_name]
        else:
            # Otherwise, can't be translated. Set value to None so the associated bit of the filter isn't applied.
            return None

        inputs = [translate(a) if op_name not in _LEAVES else a for a in op_args]

        # Handle partial application here...
        has_none = any(i is None for i in inputs)
        if has_none and op_name in _BOOLEAN_FNS:
            # if it's a logic function return all True
            return Series([True]*df.shape[0])
        elif has_none:
            # if it's any other return None
            return None

        return fn(*inputs)

    pd_filter = translate(data_filter).fillna(False)
    return df[pd_filter]


def table_dict_to_df(table_dict: Dict[str, List[Any]]) -> DataFrame:
    """Convert the table dictionary in a restriction table filter to a pandas DataFrame

    Args:
        table_dict (Dict[str, List[Any]]): the table dictionary to translate

    Returns:
        DataFrame: the equivalent dataframe

    """

    dtypes = table_dict['_DTYPES']
    df = DataFrame({k: v for k, v in table_dict.items() if k != '_DTYPES'})

    for dtype in dtypes:

        col = dtype['Name']
        dtype = SqlValType[dtype['Type']]

        if dtype == SqlValType.Int:
            df[col] = df[col].astype(int)
        elif dtype == SqlValType.Double:
            df[col] = df[col].astype(float)
        elif dtype == SqlValType.DateTime:
            df[col] = pd.to_datetime(df[col], utc=True)
        elif dtype == SqlValType.Date:
            df[col] = pd.to_datetime(df[col], utc=True)
        elif dtype == SqlValType.Boolean:
            df[col] = df[col].apply(lambda x: bool(strtobool(str(x))))

    return df
