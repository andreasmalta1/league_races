from flask import Blueprint, render_template

league_race = Blueprint("league_race", __name__)

@league_race.route("/<league>")
def league_video(league):
    file_name = f"{league}_race.mp4"
    return render_template("video.html", file_name=file_name, league=league)