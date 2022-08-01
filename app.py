from flask import Flask
from flask_mongoengine import MongoEngine
import json
from typing import Type

def create_app(config_file: str) -> Type[Flask]:
    """Returns Flask App configured with the given json file."""
    with open(config_file) as f:
        config = json.load(f)

    app = Flask(__name__)
    app.config.update(config)

    return app

def create_db(app: Type[Flask]) -> Type[MongoEngine]:
    """Returns MongoDB initialized with given Flask App instance."""
    return MongoEngine(app)

if __name__ == "__main__":
    app = create_app("config.json")
    db = create_db(app)

    # Example endpoint defined without blueprint
    @app.route("/events")
    def events():
        return "All Events"

    # Runs in DEBUG mode
    app.run()
