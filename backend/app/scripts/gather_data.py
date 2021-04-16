import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def get_standings(year: str) -> pd.DataFrame:
    nhl_standings_html = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_standings.html").text

    nhl_standings_soup = BeautifulSoup(nhl_standings_html, "html.parser")

    team_row_html = nhl_standings_soup.find(id="standings").find('tbody').find_all(class_="full_table")

    team_data = []

    for row in team_row_html:
        team_name = row.find("th").find("a").text
        team_values = [team_name] + [td.text for td in row.find_all("td")]
        team_data.append(team_values)

    col_headers = ['Team', 'GP', 'W', 'L', 'OL', 'PTS', 'PTS%', 'GF', 'GA', 'SRS', 'SOS',
                   'RPt%', 'RW', 'RgRec', 'RgPt%']

    team_data_df = pd.DataFrame(team_data, columns=col_headers)
    team_data_df["season"] = int(str(int(year) - 1) + year)

    team_data_df.to_csv('../../past_data/season_standings_current.csv', index_label=False)

    return team_data_df


def get_skater_data(year: str) -> None:
    skater_stats_html = requests.get(f"https://www.hockey-reference.com/leagues/NHL_{year}_skaters.html").text

    skater_stats_soup = BeautifulSoup(skater_stats_html, "html.parser")

    stats_row_html = skater_stats_soup.find(id="stats").find("tbody").find_all("tr")

    skater_data = []

    for row in stats_row_html:
        if not row.get("class") or "thead" not in row.get("class"):
            rk = row.find("th").text
            player_values = [rk] + [td.text for td in row.find_all("td")]
            skater_data.append(player_values)

    col_headers = ['Rk', 'Player', 'Age', 'Tm', 'Pos', 'GP', 'G', 'A', 'PTS', 'PLUSMINUS',
                   'PIM', 'PS', 'EV', 'PP', 'SH', 'GW', 'EV.1', 'PP.1', 'SH.1', 'S', 'S%',
                   'TOI', 'ATOI', 'BLK', 'HIT', 'FOW', 'FOL', 'FO%']

    skater_data_df = pd.DataFrame(skater_data, columns=col_headers)
    skater_data_df["season"] = int(str(int(year) - 1) + year)

    skater_data_df.to_csv('../../past_data/skater_stats_current.csv', index_label=False)