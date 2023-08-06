import json
import os
import unittest
from io import StringIO

import pandas as pd

from lumipy.provider.translation import apply_filter
from lumipy.test.provider.int_test_providers import PandasFilteringTestProvider


class TestFilterTranslation(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.df = PandasFilteringTestProvider(1989).df
        file_dir = os.path.dirname(os.path.abspath(__file__))
        cls.data_dir = file_dir + '/../../data/'

    def _compare_dataframes(self, test_name, test_case_name, df1, df2):

        df1 = df1.fillna('null')
        df2 = df2.fillna('null')

        self.assertEqual(
            df1.shape[0], df2.shape[0],
            msg=f'[{test_name}/{test_case_name}] dataframe row numbers did not match '
                f'(left: {df1.shape[0]} vs right: {df2.shape[0]})'
        )

        comparison = (df1.round(7) == df2.round(7))
        self.assertTrue(
            comparison.all().all(),
            msg=f"[{test_name}/{test_case_name}] dataframe cell values did not match."
        )

    def test_filter_translation(self):

        with open(self.data_dir + f'filter_test_cases.json', 'r') as f:
            filter_cases = json.load(f)

        for label, test_case in filter_cases.items():
            with self.subTest(msg=label):

                exp_df = pd.read_csv(StringIO(test_case['result']))
                exp_df['Col_D'] = pd.to_datetime(exp_df.Col_D, utc=True)

                obs_df = apply_filter(self.df, json.loads(test_case['filter'])).head(25).reset_index(drop=True)

                self._compare_dataframes('filter_translation', label, exp_df, obs_df)

    def test_filter_translation_partial_application(self):

        with open(self.data_dir + 'partial_filter_test_cases.json', 'r') as f:
            filter_cases = json.load(f)

        # Remove the last couple of columns to test partial application with missing col
        df = self.df[self.df.columns[:-2]]

        for label, test_case in filter_cases.items():
            with self.subTest(msg=label):

                filter1 = json.loads(test_case['filter1'])
                filter2 = json.loads(test_case['filter2']) if not pd.isna(test_case['filter2']) else None

                # Result from partial application of filter
                res1 = apply_filter(df, filter1)
                # Result of applying the filter equivalent
                res2 = apply_filter(df, filter2)

                self._compare_dataframes('partial_filter_translation', label, res1, res2)
