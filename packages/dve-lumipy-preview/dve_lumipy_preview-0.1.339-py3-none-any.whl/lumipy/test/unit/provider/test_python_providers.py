import datetime as dt
import io
import time
import unittest

import lumipy.provider as lp
import pandas as pd
import pytz
import requests as r
from lumipy.query.expression.sql_value_type import SqlValType
from sklearn.datasets import load_iris, load_digits, load_diabetes


def get_csv(url, params=None):
    params = {} if params is None else params
    sess = r.Session()
    with sess.post(url, json=params) as res:
        res.raise_for_status()
        csv_str = '\n'.join(map(lambda x: x.decode('utf-8'), res.iter_lines()))
        sio = io.StringIO(csv_str)
        df = pd.read_csv(sio, header=None)
        return df


class TestLocalProviderInfra(unittest.TestCase):

    def setUp(self) -> None:

        def get_df_from_load_fn(load_fn):
            data = load_fn(as_frame=True)
            return pd.concat([data['data'], data['target']], axis=1)

        self.test_dfs = {
            "Test": pd.DataFrame([{"A": i, "B": i ** 2, "C": i ** 0.5} for i in range(25)]),
            "Iris": get_df_from_load_fn(load_iris),
            "Diabetes": get_df_from_load_fn(load_diabetes),
            "Digits": get_df_from_load_fn(load_digits),
        }

    def test_local_provider_creation(self):

        for name, df in self.test_dfs.items():

            prv = lp.PandasProvider(df, name)

            self.assertEqual(len(prv.parameters), 1)
            self.assertEqual(prv.name, f'Pandas.{name}')
            self.assertEqual(prv.path_name, f'pandas-{name.lower()}')
            self.assertEqual(prv.df.shape[0], df.shape[0])
            self.assertEqual(prv.df.shape[1], df.shape[1])
            self.assertEqual(len(prv.columns), df.shape[1])

            for c1, c2 in zip(sorted(prv.columns.keys()), sorted(df.columns)):
                col = prv.columns[c1]
                self.assertEqual(col.name, str(c2).replace('.', '_'))

    def test_manager_creation(self):

        providers = []
        for name, df in self.test_dfs.items():
            providers.append(lp.PandasProvider(df, name))

        manager = lp.ProviderManager(*providers)

        # Assert api server is constructed correctly
        prs = manager.api_server.provider_roots
        self.assertEqual(manager.api_server.host, '127.0.0.1')
        self.assertEqual(manager.api_server.port, 5001)

        for pr in prs:
            name = pr['Name']
            url = pr['ApiPath']
            self.assertEqual(
                url,
                f'http://{manager.api_server.host}:{manager.api_server.port}/api/v1/{name.replace(".", "-").lower()}/'
            )

    def test_manager_operation_bernoulli(self):

        # Tests that parameters can be supplied to a provider

        providers = [lp.BernoulliDistProvider()]

        host = 'localhost'
        port = 5004
        manager = lp.ProviderManager(*providers, dry_run=True, host=host, port=port)

        with manager:
            # Test index endpoint
            res = r.get(f'http://{host}:{port}/api/v1/index')
            res.raise_for_status()
            index_json = res.json()
            self.assertEqual(len(index_json), 1)

            # Test provider metadata endpoint
            pr = manager.api_server.provider_roots[0]
            p = manager.api_server.providers[0]

            res = r.get(pr['ApiPath'] + 'metadata')
            res.raise_for_status()
            meta_json = res.json()
            self.assertEqual(len(meta_json['Columns']), len(p.columns))
            self.assertEqual(len(meta_json['Params']), len(p.parameters))
            self.assertEqual(meta_json['Name'], p.name)
            self.assertEqual(meta_json['Description'], p.description)

            # Test provider data endpoint

            df = get_csv(
                pr['ApiPath'] + 'data',
                {'params': [
                    {'name': 'Probability', 'data_type': 'Double', 'value': 0.5},
                ]}
            )
            self.assertEqual(df.shape[0], 100)
            self.assertEqual(df.shape[1], len(p.columns))

            # Test that the manager has cleaned itself and its dependencies up
        with self.assertRaises(Exception) as e:
            res = r.get(f'http://{host}:{port}')
            res.raise_for_status()

    def test_manager_operation_pandas(self):

        time.sleep(3)

        providers = [lp.PandasProvider(df, name) for name, df in self.test_dfs.items()]

        host = 'localhost'
        port = 5006

        manager = lp.ProviderManager(*providers, dry_run=True, host=host, port=port)

        with manager:

            # Test index endpoint
            res = r.get(f'http://{host}:{port}/api/v1/index')
            res.raise_for_status()
            index_json = res.json()
            self.assertEqual(len(index_json), len(manager.api_server.provider_roots))

            for p, pr in zip(providers, manager.api_server.provider_roots):
                # Test provider metadata endpoint
                res = r.get(pr['ApiPath'] + 'metadata')
                res.raise_for_status()
                meta_json = res.json()
                self.assertEqual(len(meta_json['Columns']), len(p.columns))
                self.assertEqual(len(meta_json['Params']), len(p.parameters))
                self.assertEqual(meta_json['Name'], p.name)
                self.assertEqual(meta_json['Description'], p.description)

                # Test provider data endpoint
                df = get_csv(pr['ApiPath'] + 'data')
                self.assertSequenceEqual(df.shape, p.df.shape, msg=f'{p.name} result has the wrong shape: {df.shape} vs {p.df.shape}')

        # Test that the manager has cleaned itself and its dependencies up
        with self.assertRaises(Exception) as e:
            res = r.get(f'http://{host}:{port}')
            res.raise_for_status()

    def test_pandas_provider_construction_with_datetimes(self):
        t = dt.datetime(2021, 7, 9)
        d = [{'A': k, 'T': t + dt.timedelta(days=i)} for i, k in enumerate('ABCDEFG')]
        df = pd.DataFrame(d)

        # non-tz-aware fails
        with self.assertRaises(ValueError) as ve:
            lp.PandasProvider(df, name='DatetimeTest')
            self.assertIn("Datetime values in pandas providers must be tz-aware", str(ve))
            self.assertIn("df['column'] = df['column'].dt.tz_localize(tz='utc')", str(ve))

        # tz-aware is fine and the col has the right type
        t = dt.datetime(2021, 7, 9, tzinfo=pytz.UTC)
        d = [{'A': k, 'T': t + dt.timedelta(days=i)} for i, k in enumerate('ABCDEFG')]
        df = pd.DataFrame(d)
        p = lp.PandasProvider(df, name='DatetimeTest')

        self.assertEqual(p.columns['A'].data_type, SqlValType.Text)
        self.assertEqual(p.columns['T'].data_type, SqlValType.DateTime)

    def test_manager_input_validation(self):

        time.sleep(3)

        prov = lp.PandasProvider(self.test_dfs['Test'], 'Testing')

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(dry_run=True, host='${being mean}', port=5004)

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='${being mean}', port=5004)

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='localhost', port='${being mean}')

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='localhost', port=5004, domain='${being mean}')

        with self.assertRaises(ValueError) as ve:
            lp.ProviderManager(prov, dry_run=True, host='localhost', port=5004, user='${being mean}')

    def test_setup_input_validation(self):

        with self.assertRaises(ValueError) as ve:
            lp.setup('/somewhere', version='${being mean}')

        with self.assertRaises(ValueError) as ve:
            lp.setup('/somewhere', verbosity='${being mean}')
