from flask import Flask

from src.api import story_api

app = Flask(__name__)
app.register_blueprint(story_api, url_prefix="/api")

if __name__ == "__main__":
    app.run()
