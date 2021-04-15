import os
import pandas as pd


def hello_world():
    return "Hello world!"


# If separate folders of individual CSV files need to be aggregated
def _merge_csv(source: str) -> None:
    data_folders = ["skater_stats", "season_standings", "norris_voting"]
    seasons = [filename.rstrip('.csv')[-8:] for filename in os.listdir(f"{source}/skater_stats")]

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


def read_to_dfs(source: str) -> dict:
    csv_files = [name for name in os.listdir(source) if ".csv" in name]

    dfs = {}

    for filename in csv_files:
        df = pd.read_csv(os.path.join(source, filename))
        dfs[filename.rstrip('.csv')] = df

    return dfs


read_to_dfs("../past_data")
