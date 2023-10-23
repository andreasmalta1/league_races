import bar_chart_race as bcr
import requests
import os
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip
from moviepy.editor import vfx

from leagues import LEAGUES


def get_video(df, competition_name, lge, year):
    bcr.bar_chart_race(
        df=df,
        n_bars=15,
        sort="desc",
        title=f"{competition_name} Clubs Points Since {year}",
        filename=f"videos/{lge}_clubs.mp4",
        filter_column_colors=True,
        period_length=700,
        steps_per_period=30,
        dpi=300,
        cmap="pastel1",
    )


def freeze_video(lge):
    video = (
        VideoFileClip(f"videos/{lge}_clubs.mp4")
        .fx(vfx.freeze, t="end", freeze_duration=1.5)
        .fx(vfx.multiply_speed, 0.5)
    )

    footer_one = (
        TextClip("Stats from fbref.com", font_size=25, color="black")
        .with_position((334, video.h - 75))
        .with_duration(video.duration)
        .with_start(0)
    )

    footer_two = (
        TextClip("Data Viz by @plvizstats || u/plvizstats", font_size=25, color="black")
        .with_position((330, video.h - 40))
        .with_duration(video.duration)
        .with_start(0)
    )

    if lge != "combined":
        league_id = LEAGUES[lge].get("fotmob_id")
        url = "https://images.fotmob.com/image_resources/logo/leaguelogo/"
        img_data = requests.get(f"{url}{league_id}.png").content
        with open("logo.png", "wb") as handler:
            handler.write(img_data)

        logo = (
            ImageClip("logo.png")
            .with_duration(video.duration)
            .resize(height=95)
            .margin(right=8, top=8, opacity=0)
            .with_position(("right", "top"))
        )

        final = CompositeVideoClip([video, logo, footer_one, footer_two])
    else:
        final = CompositeVideoClip([video, footer_one, footer_two])

    final.write_videofile(f"videos/{lge}_clubs_final.mp4", codec="libx264")
    if os.path.exists("logo.png"):
        os.remove("logo.png")