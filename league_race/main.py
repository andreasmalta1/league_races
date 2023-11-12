import os
import shutil
import pandas as pd

from leagues import LEAGUES
from data import get_current_season
from video import get_video, freeze_video
from dotenv import load_dotenv

load_dotenv()

CURRENT_SEASON = int(os.getenv("CURRENT_SEASON"))


def get_seasons_df(lge, year_start):
    df_all_seasons = pd.DataFrame(columns=["Season", "Squad", "Pts"])
    for year in range(year_start, CURRENT_SEASON + 1):
        df = pd.read_csv(f"csvs/{lge}/{year}-{year+1}.csv")
        df["Season"] = f"{year}/{year+1}"
        df_all_seasons = pd.concat([df_all_seasons, df], ignore_index=True)

    return df_all_seasons


def get_final_df(df):
    df = df.pivot_table(values="Pts", index=["Season"], columns="Squad")
    df.fillna(0, inplace=True)
    df.sort_values(list(df.columns), inplace=True)
    df = df.sort_index()
    df.iloc[:, 0:-1] = df.iloc[:, 0:-1].cumsum()

    return df


def leagues_point_race():
    for league in LEAGUES:
        year = LEAGUES[league].get("start_year")
        league_name = LEAGUES[league].get("lge_name")
        df = get_seasons_df(league, year)
        df = get_final_df(df)

        get_video(df, league_name, league, year)
        freeze_video(league)


def move_to_static():
    for league in LEAGUES:
        source_file = os.path.join("videos", f"{league}_race_full.mp4")
        dest_file = os.path.join(
            "..", "main_app", "static", "videos", f"{league}_race.mp4"
        )

        shutil.copy(source_file, dest_file)
        os.remove(source_file)
        os.remove(source_file.replace("_full", ""))


def main():
    get_current_season()
    leagues_point_race()
    move_to_static()


if __name__ == "__main__":
    main()

# navbar
