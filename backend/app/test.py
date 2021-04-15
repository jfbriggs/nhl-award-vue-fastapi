from scripts import preprocess
import pandas as pd
import unittest


class PreprocessTest(unittest.TestCase):
    def setUp(self):
        past_data_src = "../past_data"
        self.dfs = preprocess.read_to_dfs(past_data_src)

    def test_read_to_dfs(self):
        self.assertEqual(type(self.dfs), dict)
        self.assertEqual(len(self.dfs.keys()), 3)

        for df in self.dfs:
            self.assertEqual(type(self.dfs[df]), pd.DataFrame)

    def test_fix_names(self):
        team_names = ['Philadelphia Flyers', 'New York Islanders', 'New York Rangers',
                      'Atlanta Flames', 'Washington Capitals', 'Chicago Black Hawks',
                      'St. Louis Blues', 'Vancouver Canucks', 'Edmonton Oilers',
                      'Winnipeg Jets (Original)', 'Colorado Rockies', 'Buffalo Sabres',
                      'Boston Bruins', 'Minnesota North Stars', 'Toronto Maple Leafs',
                      'Quebec Nordiques', 'Montreal Canadiens', 'Los Angeles Kings',
                      'Pittsburgh Penguins', 'Hartford Whalers', 'Detroit Red Wings',
                      'Calgary Flames', 'New Jersey Devils', 'Chicago Blackhawks',
                      'San Jose Sharks', 'Tampa Bay Lightning', 'Ottawa Senators',
                      'Florida Panthers', 'Dallas Stars', 'Mighty Ducks of Anaheim',
                      'Colorado Avalanche', 'Phoenix Coyotes', 'Carolina Hurricanes',
                      'Nashville Predators', 'Atlanta Thrashers',
                      'Columbus Blue Jackets', 'Minnesota Wild', 'Anaheim Ducks',
                      'Winnipeg Jets (New)', 'Arizona Coyotes', 'Vegas Golden Knights']

        seasons = list(self.dfs["season_standings"]["season"].astype('str').unique())
        data_fixed = preprocess.fix_team_names(self.dfs["season_standings"], seasons)

        self.assertEqual(len(list(data_fixed["Team"].unique())) == len(team_names), True)


if __name__ == "__main__":
    unittest.main()
