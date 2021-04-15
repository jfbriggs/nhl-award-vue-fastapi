from scripts import preprocess
import pandas as pd
import unittest


class PreprocessTest(unittest.TestCase):
    def setUp(self):
        self.past_data_src = "../past_data"
        self.dfs = preprocess.read_to_dfs(self.past_data_src)

    def test_read_to_dfs(self):
        self.assertEqual(type(self.dfs), dict)
        self.assertEqual(len(self.dfs.keys()), 3)

        for df in self.dfs:
            self.assertEqual(type(self.dfs[df]), pd.DataFrame)


if __name__ == "__main__":
    unittest.main()
