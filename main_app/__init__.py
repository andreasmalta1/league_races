from flask import Flask, render_template
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

from main_app.home import home
from main_app.league_race import league_race

app.register_blueprint(home, url_prefix="/")
app.register_blueprint(league_race, url_prefix="/leagues")
