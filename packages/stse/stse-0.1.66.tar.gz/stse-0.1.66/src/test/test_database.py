import unittest
import pandas as pd
import mongomock

from stse import database as db


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.df = pd.DataFrame({
            'col1': [
                1,
                2,
                3,
                4
            ],
            'col2': [
                'a',
                'b',
                'c',
                'd'
            ]
        })

        client = mongomock.MongoClient()
        db = client['test_db']
        cls.coll = db['coll']
        
        return super().setUpClass()

    def test_df_2_db_and_db_2_df(self):
        db.df_2_db(self.df, self.coll)
        out = db.db_2_df(self.coll)
        
        self.assertEqual(
            True,
            self.df.equals(out)
        )


if __name__ == '__main__':
    unittest.main()
