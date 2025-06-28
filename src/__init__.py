from flask import Flask

from .models import db


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///parking.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from . import models  # noqa: F401

    with app.app_context():
        db.create_all()

    from .routes import bp

    app.register_blueprint(bp)

    return app
