from flask import Flask, render_template
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

@app.route('/video')
def serve_video():
    return render_template("video.html", file_name = "epl_clubs_final.mp4")