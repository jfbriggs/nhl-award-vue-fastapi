import os
import pandas as pd
from typing import List, Dict


def hello_world():
    return "Hello world!"


def get_seasons(source: str) -> List[str]:
    seasons = None

    if "skater_stats.csv" in os.listdir(source):
        stats_df = pd.read_csv(os.path.join(source, "skater_stats.csv"))
        seasons = list(stats_df["season"].astype('str').unique())
    else:
        seasons = [filename.rstrip('.csv')[-8:] for filename in os.listdir(f"{source}/skater_stats")]

    return seasons


# If separate folders of individual CSV files need to be aggregated
def _merge_csv(source: str) -> None:
    data_folders = ["skater_stats", "season_standings", "norris_voting"]
    seasons = get_seasons(source)

    dataframes = {}

    for season in seasons:
        for folder in data_folders:
            df = pd.read_csv(f"{source}/{folder}/{folder}_{season}.csv")
            df["season"] = season
            if dataframes.get(folder) is None:
                dataframes[folder] = df
            else:
                dataframes[folder] = pd.concat([dataframes[folder], df]).reset_index(drop=True)

    for df_name in dataframes:
        dataframes[df_name].to_csv(os.path.join(source, f"{df_name}.csv"), index=False)


# Convert aggregated CSVs to separate dataframes
def read_to_dfs(source: str) -> dict:
    csv_files = [name for name in os.listdir(source) if ".csv" in name]

    dataframes = {}

    for filename in csv_files:
        df = pd.read_csv(os.path.join(source, filename))
        name = filename.split('.')[0]
        dataframes[name] = df

    return dataframes


# Fix team name values, including apply proper Winnipeg Jets names
def fix_team_names(team_data: pd.DataFrame, seasons: List[str]) -> pd.DataFrame:
    # Fix team name values
    replace_values = {
        "ampa Bay Lightning": "Tampa Bay Lightning",
        "ew Jersey Devils": "New Jersey Devils",
        "hicago Black Hawks": "Chicago Black Hawks",
        "hiladelphia Flyers": "Philadelphia Flyers",
        "innesota North Stars": "Minnesota North Stars",
        "ontreal Canadiens": "Montreal Canadiens",
        "orida Panthers": "Florida Panthers"
    }

    team_data = team_data.copy().replace({"Team": replace_values})

    # fix Jets rows to distinguish old org from new
    def replace_jets(row):
        new_jets_start = seasons.index("20112012")

        if row["Team"] == "Winnipeg Jets":
            if row["season"] in seasons[new_jets_start:]:  # for seasons 20112012 and later
                row["Team"] = "Winnipeg Jets (New)"
            else:
                row["Team"] = "Winnipeg Jets (Original)"

        return row

    team_data = team_data.apply(replace_jets, axis=1)

    return team_data


def replace_names_abbrevs(team_data: pd.DataFrame) -> pd.DataFrame:
    team_abbrevs = {
        "Anaheim Ducks": "ANA",
        "Arizona Coyotes": "ARI",
        "Atlanta Flames": "ATF",
        "Atlanta Thrashers": "ATL",
        "Boston Bruins": "BOS",
        "Buffalo Sabres": "BUF",
        "Carolina Hurricanes": "CAR",
        "Chicago Black Hawks": "CBH",
        "Columbus Blue Jackets": "CBJ",
        "Calgary Flames": "CGY",
        "Chicago Blackhawks": "CHI",
        "Colorado Rockies": "CLR",
        "Colorado Avalanche": "COL",
        "Dallas Stars": "DAL",
        "Detroit Red Wings": "DET",
        "Edmonton Oilers": "EDM",
        "Florida Panthers": "FLA",
        "Hartford Whalers": "HAR",
        "Los Angeles Kings": "LAK",
        "Mighty Ducks of Anaheim": "MDA",
        "Minnesota Wild": "MIN",
        "Minnesota North Stars": "MNS",
        "Montreal Canadiens": "MTL",
        "New Jersey Devils": "NJD",
        "Nashville Predators": "NSH",
        "New York Islanders": "NYI",
        "New York Rangers": "NYR",
        "Ottawa Senators": "OTT",
        "Philadelphia Flyers": "PHI",
        "Phoenix Coyotes": "PHX",
        "Pittsburgh Penguins": "PIT",
        "Quebec Nordiques": "QUE",
        "San Jose Sharks": "SJS",
        "St. Louis Blues": "STL",
        "Tampa Bay Lightning": "TBL",
        "Toronto Maple Leafs": "TOR",
        "Vancouver Canucks": "VAN",
        "Vegas Golden Knights": "VEG",
        "Winnipeg Jets (Original)": "WIN",
        "Winnipeg Jets (New)": "WPG",
        "Washington Capitals": "WSH"
    }

    team_data = team_data.copy().replace(team_abbrevs)

    return team_data


def convert_duplicates(skater_data: pd.DataFrame) -> pd.DataFrame:
    skater_data = skater_data.copy()

    # identify all multi-team players (in most cases, players who were traded during a season)
    # by filtering dataframe to entries with "TOT" as the team
    traded_players = skater_data[skater_data["Tm"] == "TOT"]

    # crate a list that contains just the names and seasons, which we can iterate through
    traded_players_list = [(row[0], row[1]) for row in traded_players[["Player", "season"]].values]

    # create a list and populate with the team abbreviations that represent replacement values for "TOT" for each player + season
    team_most_games = []

    for player, season in traded_players_list:
        player_data = skater_data.loc[
            (skater_data["Player"] == player) & (skater_data["season"] == season) & (
                    skater_data["Tm"] != "TOT")].copy()
        # sort each individual player's DF by games played first, then PLUSMINUS > points if GP the same for multiple rows
        player_data = player_data.sort_values(by=["GP", "PLUSMINUS", "PTS"], ascending=False)
        team_most_games.append(player_data.iloc[0]["Tm"])

    # now replace "TOT" values in the original defensemen dataframe with the updated team abbreviation values
    skater_data.loc[skater_data["Tm"] == "TOT", "Tm"] = team_most_games

    skater_data = skater_data.drop_duplicates(subset=["season", "Rk"], keep="last")

    return skater_data


def pre_merge_preprocess(dfs: Dict[str, pd.DataFrame], source: str) -> Dict[str, pd.DataFrame]:
    seasons = get_seasons(source)

    # remove asterisks from team names
    dfs["season_standings"]["Team"] = dfs["season_standings"]["Team"].str.replace("*", "")
    dfs["skater_stats"]["Player"] = dfs["skater_stats"]["Player"].str.replace("*", "")
    dfs["norris_voting"]["Player"] = dfs["norris_voting"]["Player"].str.replace("*", "")

    # Adjust team names in standings data
    dfs["season_standings"] = fix_team_names(dfs["season_standings"], seasons)

    # replace team names with abbrevs in standings data
    dfs["season_standings"] = replace_names_abbrevs(dfs["season_standings"])

    # filter player data to defensemen only
    dfs["skater_stats"] = dfs["skater_stats"][dfs["skater_stats"]["Pos"] == "D"].copy().sort_values(
        by=["season", "Player", "GP"]).reset_index(drop=True)

    # deal with duplicates (traded players)
    dfs["skater_stats"] = convert_duplicates(dfs["skater_stats"].copy())

    return dfs
