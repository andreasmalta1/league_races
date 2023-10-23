import pandas as pd

from leagues import LEAGUES
from video import get_video, freeze_video


def get_seasons_df(lge, year_start):
    df_all_seasons = pd.DataFrame(columns=["Season", "Squad", "Pts"])
    for year in range(year_start, 2022):
        df = pd.read_csv(f"csvs/{lge}/league_standings/{lge}_{year}-{year+1}.csv")
        df = df[["Squad", "Pts"]]
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
    for lge in LEAGUES:
        if not LEAGUES[lge].get("start_year"):
            continue

        year = LEAGUES[lge].get("start_year")
        lge_name = LEAGUES[lge].get("lge_name")
        df = get_seasons_df(lge, year)
        df = get_final_df(df)

        get_video(df, lge_name, lge, year)
        freeze_video(lge)

    df = get_final_df(pd.read_csv(f"csvs/combined_league_standings.csv"))
    get_video(df, "Combined Top 5 Leagues", "combined", 1995)
    freeze_video("combined")