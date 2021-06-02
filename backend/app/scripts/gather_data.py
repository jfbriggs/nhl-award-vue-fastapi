import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_standings_data(year: str) -> pd.DataFrame:
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

    return team_data_df


def get_skater_data(year: str) -> pd.DataFrame:
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

    return skater_data_df


def get_current_data(year: str) -> None:
    standings_df = get_standings_data(year)
    skater_df = get_skater_data(year)

    standings_df.to_csv('../data/season_standings_current.csv', index_label=False)
    skater_df.to_csv('../data/skater_stats_current.csv', index_label=False)

    print("Current season's data updated.")


# Get player IDs, team abbrevs, and jersey numbers from NHL Stats API
def get_nhl_players() -> dict:
    teams_players = requests.get("https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster").json()["teams"]
    # players = {}

    teams = {}

    for team in teams_players:
        roster = {}

        try:
            for player in team["roster"]["roster"]:
                if player["position"]["code"] == "D":
                    roster[player["person"]["id"]] = {
                        "name": player["person"]["fullName"],
                        "team_dashed": '-'.join(team["name"].lower().replace("é", "e").replace('.', '').split()),
                        "team_full": team["name"],
                        "jersey_number": player.get("jerseyNumber")
                    }
        except KeyError:  # account for possible KeyError when team["roster"] doesn't exit (Seattle - new franchise, no roster)
            pass

        teams[team["abbreviation"]] = roster

    return teams


def get_past_winners(name: str) -> list:
    winners_html = requests.get("https://www.hockey-reference.com/awards/norris.html").text
    winners_soup = BeautifulSoup(winners_html, 'html.parser')
    winners_rows = winners_soup.select(f'#{name}')[0].find_all('tbody')[0].find_all('tr')

    winners = []

    for row in winners_rows:
        data = list(map(lambda x: x.text, row.find_all(['th', 'td'], {'data-stat': ['season', 'player', 'team_id']})))
        winners.append(data)

    return winners
