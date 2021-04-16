import os
import warnings

import pandas as pd
from typing import List, Dict, Tuple

from sklearn.preprocessing import minmax_scale, LabelEncoder


def hello_world():
    return "Hello world!"


# Get list of all seasons included in past (non-current season's) data
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
    past_csv_files = [name for name in os.listdir(source) if ".csv" in name and "current" not in name]
    current_csv_Files = [name for name in os.listdir(source) if ".csv" in name and "current" in name]

    dataframes = {}

    # read past data into DFs
    for filename in past_csv_files:
        df = pd.read_csv(os.path.join(source, filename))
        name = filename.split('.')[0]
        dataframes[name] = df

    return dataframes


# Fix team name values, including apply proper Winnipeg Jets names
def fix_team_names(team_data: pd.DataFrame) -> pd.DataFrame:
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

    seasons = list(team_data["season"].unique())

    # fix Jets rows to distinguish old org from new
    def replace_jets(row):
        new_jets_start = seasons.index(20112012)

        if row["Team"] == "Winnipeg Jets":
            if row["season"] in seasons[new_jets_start:]:  # for seasons 20112012 and later
                row["Team"] = "Winnipeg Jets (New)"
            else:
                row["Team"] = "Winnipeg Jets (Original)"

        return row

    team_data = team_data.apply(replace_jets, axis=1)

    return team_data


# Replace full team names with team abbreviations
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


# Eliminates multiple entries for players (i.e. due to being traded mid-season
def convert_multiples(skater_data: pd.DataFrame) -> pd.DataFrame:
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


# Run dataframes through all pre-merge preprocessing steps
def pre_merge_preprocess(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    # remove asterisks from team names
    dfs["season_standings"]["Team"] = dfs["season_standings"]["Team"].str.replace("*", "")
    dfs["skater_stats"]["Player"] = dfs["skater_stats"]["Player"].str.replace("*", "")
    dfs["norris_voting"]["Player"] = dfs["norris_voting"]["Player"].str.replace("*", "")

    # Adjust team names in standings data
    dfs["season_standings"] = fix_team_names(dfs["season_standings"])

    # replace team names with abbrevs in standings data
    dfs["season_standings"] = replace_names_abbrevs(dfs["season_standings"])

    # filter player data to defensemen only
    dfs["skater_stats"] = dfs["skater_stats"][dfs["skater_stats"]["Pos"] == "D"].copy().sort_values(
        by=["season", "Player", "GP"]).reset_index(drop=True)

    # deal with multiples (traded players)
    dfs["skater_stats"] = convert_multiples(dfs["skater_stats"].copy())

    return dfs


# Merge dataframes into one, dropping duplicate columns along the way
def merge_dataframes(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    players_teams_data = dfs["skater_stats"].merge(dfs["season_standings"], how="left", left_on=["season", "Tm"],
                                                   right_on=["season", "Team"], suffixes=("_player", "_team"))
    voting_data = dfs["norris_voting"].drop(["Age", "Tm", "Pos", "G", "A", "PTS", "PLUSMINUS", "PS"], axis=1)
    all_merged_data = players_teams_data.merge(voting_data, how="left", left_on=["season", "Player"],
                                               right_on=["season", "Player"])

    return all_merged_data


# Drop columns that won't be used for modeling
def drop_unused_cols(df: pd.DataFrame) -> pd.DataFrame:
    # create list of column names that will be dropped from the dataframe
    columns_to_drop = [
        "Rk",
        "Pos",
        "FOW",
        "FOL",
        "FO%",
        "Team",
        "GP_team",
        "W",
        "L",
        "OL",
        "PTS%",
        "GF",
        "GA",
        "SRS",
        "SOS",
        "RPt%",
        "RW",
        "RgRec",
        "RgPt%",
        "Place",
        "Vote%",
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "OPS",
        "DPS",
        "GPS"
    ]

    # create a copy of the dataframe post-dropping of columns
    pared_data = df.drop(columns_to_drop, axis=1).copy()

    return pared_data


# Apply remaining column cleanup/adjustments
def adjust_remaining_cols(df: pd.DataFrame) -> pd.DataFrame:
    # create dictionary for substitutions
    abbrev_subs = {
        "PHX": "ARI",  # Phoenix Coyotes became Arizona Coyotes
        "MDA": "ANA",  # Mighty Ducks of Anaheim became Anaheim Ducks
        "CBH": "CHI"  # Chicago Black Hawks became Chicago Blackhawks
    }

    # apply substitutions
    df["Tm"] = df["Tm"].replace(abbrev_subs)

    # fix nulls in Votes column
    df.loc[df["Votes"].isnull(), "Votes"] = 0

    # convert Votes to percentage of total, excluding current season
    for season in df["season"].unique():
        season_vote_data = df.loc[df["season"] == season, "Votes"]
        season_vote_data = season_vote_data / season_vote_data.sum()
        df.loc[df["season"] == season, "Votes"] = season_vote_data

    # fix ATOI column datatype/values
    df["ATOI"] = df["TOI"] / df["GP_player"]

    # create dictionary for column label substitutions
    new_column_labels = {
        "Player": "name",
        "Age": "age",
        "Tm": "team",
        "GP_player": "games_played",
        "G": "goals",
        "A": "assists",
        "PTS_player": "points",
        "PLUSMINUS": "plus_minus",
        "PIM": "penalty_minutes",
        "PS": "point_share",
        "EV": "even_strength_goals",
        "PP": "power_play_goals",
        "SH": "shorthanded_goals",
        "GW": "game_winning_goals",
        "EV.1": "even_strength_assists",
        "PP.1": "power_play_assists",
        "SH.1": "shorthanded_assists",
        "S": "shots",
        "S%": "shooting_pct",
        "TOI": "total_toi",
        "ATOI": "avg_toi",
        "BLK": "blocked_shots",
        "HIT": "hits",
        "PTS_team": "team_standings_pts",
        "Votes": "norris_point_pct",
    }

    # apply substitutions and check new column labels
    df.rename(new_column_labels, axis=1, inplace=True)

    return df


# Handle missing values in shooting_pct and blocked_shots columns
def fix_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[df["shooting_pct"].isnull(), "shooting_pct"] = 0

    blocked_shots_missing = (df["blocked_shots"].isnull()) & (df["hits"].notnull())
    # insert 0 for blocked_shots value where missing
    df.loc[blocked_shots_missing, "blocked_shots"] = 0

    return df


# Add per-game and per-60 features
def generate_features(df: pd.DataFrame) -> pd.DataFrame:
    stats_to_average = ["goals", "assists", "points", "blocked_shots", "hits"]
    pg_suffix = "_per_game"
    p60_suffix = "_per_60"

    for stat in stats_to_average:
        pg_label = stat + pg_suffix
        df[pg_label] = df[stat] / df["games_played"]

        p60_label = stat + p60_suffix
        df[p60_label] = df[stat] / (df["total_toi"] / 60)

    return df


# Rescale continuous variables to establish equivalency between seasons (using min-max scaling)
def rescale_continuous(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["age", "games_played", "goals", "assists", "points", "plus_minus", "penalty_minutes",
            "point_share", "even_strength_goals", "power_play_goals", "shorthanded_goals",
            "game_winning_goals", "even_strength_assists", "power_play_assists", "shorthanded_assists",
            "shots", "shooting_pct", "total_toi", "avg_toi", "blocked_shots", "hits", "team_standings_pts",
            "goals_per_game", "goals_per_60", "assists_per_game", "assists_per_60", "points_per_game",
            "points_per_60", "blocked_shots_per_game", "blocked_shots_per_60", "hits_per_game",
            "hits_per_60"]

    with warnings.catch_warnings():
        # temporarily ignore RuntimeWarning for trying to rescale segments of data with NaN values
        warnings.filterwarnings("ignore", category=RuntimeWarning)

        for season in df["season"].unique():
            season_cols = df.loc[df["season"] == season, cols].copy()
            rescaled_data = minmax_scale(season_cols)
            df.loc[df["season"] == season, cols] = rescaled_data

    return df


# Encode (convert to numeric) team column and output encodings to make available for other functionality
def encode_categorical(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
    # encode team column -> convert to integers for use with tree-based models
    encoder = LabelEncoder()
    df["team"] = encoder.fit_transform(df["team"])

    team_encodings = {i: val for i, val in enumerate(encoder.classes_)}

    return df, team_encodings


# Filter data to subset that will be used for training model
def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    toi_idx = df[df["total_toi"].notnull()].head(1).index.values[0]

    # filter data to when TOI/ATOI started being tracked (index 4388)
    filtered_data = df.loc[toi_idx:].copy()

    # remove columns with null values left
    filtered_data = filtered_data.dropna(axis=1)

    return filtered_data


# Apply all post-merge preprocessing steps, using make_pipeline as applicable
def post_merge_preprocess(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:

    post_merge_pipe = make_pipeline([drop_unused_cols, adjust_remaining_cols, fix_missing_values, generate_features, rescale_continuous])

    data = post_merge_pipe(df)
    data, encodings = encode_categorical(data)
    data = filter_data(data)

    return data, encodings


# Create a pipeline of functions
def make_pipeline(funcs: List[callable]) -> callable:
    def inner(inp):
        curr_val = inp
        for f in funcs:
            curr_val = f(curr_val)

        return curr_val

    return inner


# Create pipeline of data conversion and preprocessing/merge steps up to multiple parameter funcs, output final data and encodings
def merge_process(source: str) -> Tuple[pd.DataFrame, dict]:
    process_pipe = make_pipeline([read_to_dfs, pre_merge_preprocess, merge_dataframes, post_merge_preprocess])
    data, encodings = process_pipe(source)

    return data, encodings
