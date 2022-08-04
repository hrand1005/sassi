from flask import Flask
from flask_mongoengine import MongoEngine
import json
from typing import Type

def create_app() -> Type[Flask]:
    """Returns Flask App configured with the given json file."""
    with open("config.json") as f:
        config = json.load(f)

    app = Flask(__name__)
    app.config.update(config)

    from models.db import db
    db.init_app(app)

    from api.hello import bp
    app.register_blueprint(bp)

    from api.user import bp
    app.register_blueprint(bp)

    return app

if __name__ == "__main__":
    app = create_app()

    # Runs in DEBUG mode
    app.run()
