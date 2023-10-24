import os
from bar_chart_race import bar_chart_race
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip, vfx


def get_video(df, competition_name, league, year):
    bar_chart_race(
        df=df,
        n_bars=15,
        sort="desc",
        title=f"{competition_name} Clubs Points Since {year}",
        filename=os.path.join("videos", f"{league}_race.mp4"),
        filter_column_colors=True,
        period_length=700,
        steps_per_period=30,
        dpi=300,
        cmap="pastel1",
    )


def freeze_video(league):
    video = (
        VideoFileClip(os.path.join("videos", f"{league}_race.mp4"))
        .fx(vfx.freeze, t="end", freeze_duration=1.5)
        .fx(vfx.multiply_speed, 0.5)
    )

    footer_one = (
        TextClip("Data from fbref.com", font_size=25, color="black")
        .with_position((334, video.h - 50))
        .with_duration(video.duration)
        .with_start(0)
    )

    logo = (
        ImageClip(os.path.join("logos", f"{league}.png"), transparent=True)
        .with_duration(video.duration)
        .resize(height=95)
        .margin(right=8, top=8, opacity=0)
        .with_position(("right", "top"))
    )

    final = CompositeVideoClip([video, logo, footer_one])

    final.write_videofile(
        os.path.join("videos", f"{league}_race_full.mp4"), codec="libx264"
    )
