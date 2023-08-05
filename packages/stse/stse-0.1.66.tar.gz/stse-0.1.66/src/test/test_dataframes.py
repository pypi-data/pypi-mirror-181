import unittest
import pandas as pd
import numpy as np
import json

from stse import dataframes


class TestDataframes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_df = pd.DataFrame({'a': [4, '5', '6'], 'b': ['6', '5', '4']})
        cls.mol_test_df = pd.DataFrame({'SMILES': [4, '5', '6'], 'Molecule': ['6', '5', '4'], 'InChi': [5, 6, 8]})
        cls.nan_test_df = pd.DataFrame({'a': ['', '5', '6'], 'b': ['a', '8', 'None']})
        cls.blank_solution = pd.DataFrame({'a': [np.nan, '5', '6'], 'b': ['a', '8', np.nan]})
        cls.non_num_solution = pd.DataFrame({'a': [np.nan, '5', '6'], 'b': [np.nan, '8', np.nan]})
        return super().setUpClass()
    
    def test_drop_val(self):
        # Test number
        dropped1 = dataframes.drop_val(self.test_df, 'a', 4)
        assert dropped1.equals(pd.DataFrame({'a': ['5', '6'], 'b': ['5', '4']}))
        
        # Test string
        dropped2 = dataframes.drop_val(self.test_df, 'a', '4')
        assert dropped2.equals(self.test_df)
        
        # Test b column
        dropped3 = dataframes.drop_val(self.test_df, 'b', '4')
        assert dropped3.equals(pd.DataFrame({'a': [4, '5'], 'b': ['6', '5']}))
        
    def test_pull_val(self):
        # Test number
        pulled1 = dataframes.pull_val(self.test_df, 'a', 4)
        assert pulled1.equals(pd.DataFrame({'a': [4], 'b': ['6']}).astype(object))
        
        # Test string
        pulled2 = dataframes.pull_val(self.test_df, 'a', '6')
        assert pulled2.equals(pd.DataFrame({'a': ['6'], 'b': ['4']}, index=[2]))
        
        # Test b column
        pulled3 = dataframes.pull_val(self.test_df, 'b', '5')
        assert pulled3.equals(pd.DataFrame({'a': ['5'], 'b': ['5']}, index=[1]))
        
    def test_pull_not_val(self):
        # Test number
        pulled1 = dataframes.pull_not_val(self.test_df, 'a', 4)
        assert pulled1.equals(pd.DataFrame({'a': ['5', '6'], 'b': ['5', '4']}, index=[1, 2]).astype(object))
        
        # Test string
        pulled2 = dataframes.pull_not_val(self.test_df, 'a', '6')
        assert pulled2.equals(pd.DataFrame({'a': [4, '5'], 'b': ['6', '5']}))
        
        # Test b column
        pulled3 = dataframes.pull_not_val(self.test_df, 'b', '5')
        assert pulled3.equals(pd.DataFrame({'a': [4, '6'], 'b': ['6', '4']}, index=[0, 2]))
        
        # Test pull invalid number --> returns what was input
        pulled4 = dataframes.pull_not_val(self.test_df, 'b', '3')
        assert pulled4.equals(self.test_df)
        
    def test_id_nearest_col(self):
        # Test similar variations
        assert dataframes.id_nearest_col(self.mol_test_df, 'smiles') == 'SMILES'
        assert dataframes.id_nearest_col(self.mol_test_df, 'smIles') == 'SMILES'
        assert dataframes.id_nearest_col(self.mol_test_df, 'smes') == 'SMILES'
        
        # Test null return
        assert dataframes.id_nearest_col(self.mol_test_df, 's') == None
        
    def test_remove_header_chars(self):
        test_df1 = self.mol_test_df.copy()
        test_df2 = self.mol_test_df.copy()
        test_df3 = self.mol_test_df.copy()
        test_df1.columns = ['MILE', 'Molecule', 'InChi']
        test_df2.columns = ['SMLES', 'Molecule', 'nCh']
        test_df3.columns = ['SMILES', 'Molecule', 'InCh']
        
        # Test w/ case sensitive on
        assert dataframes.remove_header_chars(self.mol_test_df, 's').equals(test_df1)
        assert dataframes.remove_header_chars(self.mol_test_df, 'S').equals(test_df1)
        
        # Test w/ case sensitive off
        assert dataframes.remove_header_chars(self.mol_test_df, 's', case_insensitive=False).equals(self.mol_test_df)
        assert dataframes.remove_header_chars(self.mol_test_df, 'S', case_insensitive=False).equals(test_df1)
        
        # Test multiple instances
        assert dataframes.remove_header_chars(self.mol_test_df, 'i').equals(test_df2)
        assert dataframes.remove_header_chars(self.mol_test_df, 'i', case_insensitive=False).equals(test_df3)
        
    def test_convert_to_nan(self):
        # Test replace nan
        na_df = dataframes.convert_to_nan(self.nan_test_df)
        assert na_df.equals(self.blank_solution)
        
        # Test case sensitivity
        na_df = dataframes.convert_to_nan(self.nan_test_df, na=('A'))
        assert na_df.equals(pd.DataFrame({'a': ['', '5', '6'], 'b': [np.nan, '8', 'None']}))
        
    def test_non_num_to_nan(self):
        # Test on only first column
        na_df = dataframes.non_num_to_nan(self.nan_test_df, self.nan_test_df.columns[0])
        assert na_df.equals(pd.DataFrame({'a': [np.nan, '5', '6'], 'b': ['a', '8', 'None']}))
        
        # Test on only second column (unchanged)
        na_df = dataframes.non_num_to_nan(self.nan_test_df, self.nan_test_df.columns[1])
        assert na_df.equals(self.nan_test_df)
        
        # Test on both columns
        na_df = dataframes.non_num_to_nan(self.nan_test_df, self.nan_test_df.columns)
        assert na_df.equals(self.non_num_solution)
        
    def test_nan_col_indices(self):
        # Test each col separately
        assert dataframes.nan_col_indices(self.blank_solution, self.blank_solution.columns[0]) == [0]
        assert dataframes.nan_col_indices(self.blank_solution, self.blank_solution.columns[1]) == [2]
        
    def test_remove_nan_cols(self):
        nan_col_df = self.test_df.copy()
        
        # Append new columns
        nan_col_df['c'] = 3*['None']
        nan_col_df['d'] = 3*['nan']
        nan_col_df['e'] = 3*['']
        nan_col_df['f'] = 3*[np.nan]
        
        # Check new columns were added successfully
        assert len(nan_col_df.columns) == 6
        
        # Test blank column removal
        assert dataframes.remove_nan_cols(nan_col_df).equals(self.test_df)
        
    def test_remove_nan_rows(self):
        self.non_num_solution = pd.DataFrame({'a': [np.nan, '5', '6'], 'b': [np.nan, '8', np.nan]})
        
        col_a = dataframes.remove_nan_rows(self.blank_solution, ['a'])
        assert col_a.equals(pd.DataFrame({'a': ['5', '6'], 'b': ['8', np.nan]}))
        
        col_b = dataframes.remove_nan_rows(self.blank_solution, ['b'])
        assert col_b.equals(pd.DataFrame({'a': [np.nan, '5'], 'b': ['a', '8']}))
        
        both_cols = dataframes.remove_nan_rows(self.blank_solution, self.blank_solution.columns)
        assert both_cols.equals(pd.DataFrame({'a': ['5'], 'b': ['8']}))
        
    def test_df_2_json(self):
        out = dataframes.df_2_json(self.test_df)
        expected = '[[4, "6"], ["5", "5"], ["6", "4"]]'
        
        self.assertEqual(
            out,
            expected
        )
        
        # Ensure valid json
        try:
            json.loads(out)
        except Exception as e:
            self.fail(e)
            
    def test_z_norm(self):
        test_df = pd.DataFrame({
            'a': [1, 4, 7],
            'b': [5, 9, 10]
        })
        z_norm_df = dataframes.z_norm(test_df)
        
        # Zero mean
        self.assertFalse(
            np.allclose(
                test_df.mean(),
                np.array(2*[0], dtype=float)
            )
        )
        self.assertTrue(
            np.allclose(
                z_norm_df.mean(),
                np.zeros(2)
            )
        )
        
        # Standard dev. of 1
        self.assertFalse(
            np.allclose(
                test_df.std(),
                np.ones(2)
            )
        )
        self.assertTrue(
            np.allclose(
                z_norm_df.std(),
                np.ones(2)
            )
        )
        
    def test_compare(self):
        inner = pd.DataFrame({
            'a': [1, 2, 3, 4],
            'b': [2, 3, 5, 6],
        })
        outer = pd.DataFrame({
            'c': [2, 3, 5, 6, 7, 8, 9, 10]
        })
        
        # Find same
        expected = outer.iloc[:2]
        out = dataframes.compare(inner, outer, 'a', 'c', find_same=True)
        self.assertTrue(
            out.equals(expected)
        )

        # Try with combine_headers
        expected = pd.concat((outer.iloc[:2], inner.iloc[1:3].reset_index(drop=True)), axis=1)
        out = dataframes.compare(inner, outer, 'a', 'c', find_same=True, combine_headers=True)
        self.assertTrue(
            out.equals(expected)
        )
        
        # Find unique
        expected = outer.iloc[2:]
        out = dataframes.compare(inner, outer, 'a', 'c', find_same=False)
        self.assertTrue(
            out.equals(expected)
        )
    
    def test_concat(self):
        df1 = pd.DataFrame({
            'a': [1, 2, 3],
            'c': [4, 5, 6],
            'b': [7, 8, 9]
        })
        df2 = pd.DataFrame({
            'b': [10, 11],
            'c': [13, 14],
            'd': [16, 17]
        })
        
        # Drop uncommon
        expected1 = pd.DataFrame({
            'b': [7, 8, 9, 10, 11],
            'c': [4, 5, 6, 13, 14]
        })
        out1 = dataframes.concat([df1, df2], drop_uncommon_columns=True)
        self.assertTrue(
            out1.equals(expected1)
        )
        
        # Keep uncommon, replace blank w/ nan
        expected2 = pd.DataFrame({
            'a': [1, 2, 3, np.nan, np.nan],
            'b': [7, 8, 9, 10, 11],
            'c': [4, 5, 6, 13, 14],
            'd': [np.nan, np.nan, np.nan, 16, 17]
        })
        out2 = dataframes.concat([df1, df2], drop_uncommon_columns=False)
        self.assertTrue(
            out2.equals(expected2)
        )
        
        # Dropna is possible
        self.assertTrue(
            out2.dropna(axis=1).equals(expected1)
        )
        
    def test_sync_na_drop(self):
        df1 = pd.DataFrame({
            'one': [1, np.nan, 3],
            'b': [4, np.nan, np.nan],
            'c': [7, 8, 9]
        })
        iter1 = ['a', 'b', 'c']
        
        # One column
        out_df1, out_iter1 = dataframes.sync_na_drop(df1, 'one', iter1, all_na=True)
        out_df2, out_iter2 = dataframes.sync_na_drop(df1, 'one', iter1, all_na=False)
        
        self.assertTrue(
            out_df1.equals(
                df1.dropna(subset=['one'])
            )
        )
        self.assertTrue(  # Same bc only one column
            out_df1.equals(
                out_df2
            )
        )
        self.assertEqual(
            out_iter1,
            ['a', 'c'],
            out_iter2
        )
        
        # Two columns, all_na=True
        out_df3, out_iter3 = dataframes.sync_na_drop(df1, ['one', 'c'], iter1, all_na=True)
        
        self.assertTrue(  # No change
            out_df3.equals(
                df1
            )
        )
        self.assertEqual(  # No change
            out_iter3,
            iter1
        )
        
        # Two columns, all_na=False
        out_df4, out_iter4 = dataframes.sync_na_drop(df1, ['one', 'c'], iter1, all_na=False)
        
        self.assertTrue(
            out_df4.equals(
                df1.dropna(subset=['one'])
            )
        )
        self.assertEqual(
            out_iter4,
            ['a', 'c']
        )
        
        # 'a' and 'b' columns, all_na=True
        out_df5, out_iter5 = dataframes.sync_na_drop(df1, ['one', 'b'], iter1, all_na=True)
        
        self.assertTrue(
            out_df5.equals(
                df1.dropna(subset=['one', 'b'], how='all')
            )
        )
        self.assertEqual(
            out_iter5,
            ['a', 'c']
        )
        
        # a' and 'b' columns, all_na=False
        out_df6, out_iter6 = dataframes.sync_na_drop(df1, ['one', 'b'], iter1, all_na=False)
        
        self.assertTrue(
            out_df6.equals(
                df1.dropna(subset=['one', 'b'], how='any')
            )
        )
        self.assertEqual(
            out_iter6,
            ['a']
        )
        
        # Multiple iterables
        iter2 = ['d', 'e', 'f']
        _, out_iter7 = dataframes.sync_na_drop(df1, ['one', 'b'], iter1, iter2, all_na=False)
        
        self.assertEqual(
            out_iter7,
            [
                ['a'],
                ['d']
            ]
        )
        
        # Raise length error
        iter3 = 5*['h']
        with self.assertRaises(ValueError):
            dataframes.sync_na_drop(df1, ['one', 'b'], iter1, iter3, all_na=True)
        

if __name__ == '__main__':
    unittest.main()
