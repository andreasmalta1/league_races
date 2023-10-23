from flask import Flask, send_file
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = getenv("SECRET_KEY")

@app.route('/video')
def serve_video():
    # Define the path to the latest generated video
    video_path = "path/to/your/generated_video.mp4"
    return send_file(video_path, as_attachment=True)