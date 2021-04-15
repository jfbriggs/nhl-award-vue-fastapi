from scripts import preprocess
import pandas as pd
import unittest


class PreprocessTest(unittest.TestCase):
    def setUp(self):
        self.past_data_src = "../past_data"

    def test_read_to_dfs(self):
        dfs = preprocess.read_to_dfs(self.past_data_src)

        self.assertEqual(type(dfs), dict)
        self.assertEqual(len(dfs.keys()), 3)

        for df in dfs:
            self.assertEqual(type(dfs[df]), pd.DataFrame)


if __name__ == "__main__":
    unittest.main()