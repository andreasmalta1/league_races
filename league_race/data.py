import os
import pandas as pd
import time
from dotenv import load_dotenv

from leagues import LEAGUES

load_dotenv()

LEAGUE_URL = "https://fbref.com/en/comps/{league_code}/{season_start}-{season_end}/{season_start}-{season_end}-{league_name}-Stats"
CURRENT_SEASON = int(os.getenv("CURRENT_SEASON"))


def get_league_data(league, file_path):
    league_code = LEAGUES[league]["lge_code"]
    league_name = LEAGUES[league]["lge_name"]
    season_start = LEAGUES[league]["start_year"]

    for year in range(season_start, CURRENT_SEASON + 1):
        league_url = LEAGUE_URL.format(
            league_code=league_code[1:],
            season_start=year,
            season_end=year + 1,
            league_name=league_name.replace(" ", "-"),
        )

        html = pd.read_html(league_url, header=0)
        df = html[0][["Squad", "Pts"]]
        df.to_csv(os.path.join(file_path, f"{year}-{year+1}.csv"))

        time.sleep(60)


def get_previous_seasons_data():
    for league in LEAGUES:
        file_path = os.path.join("csvs", league)
        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        get_league_data(league, file_path)


def get_current_season():
    for league in LEAGUES:
        print(league)
        file_path = os.path.join("csvs", league)
        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        league_code = LEAGUES[league]["lge_code"]
        league_name = LEAGUES[league]["lge_name"]

        league_url = LEAGUE_URL.format(
            league_code=league_code[1:],
            season_start=CURRENT_SEASON,
            season_end=CURRENT_SEASON + 1,
            league_name=league_name.replace(" ", "-"),
        )

        html = pd.read_html(league_url, header=0)
        df = html[0][["Squad", "Pts"]]
        df.to_csv(os.path.join(file_path, f"{CURRENT_SEASON}-{CURRENT_SEASON+1}.csv"))
