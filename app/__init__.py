from flask import Flask
from flask_cors import CORS
from .database import db
from .utils import bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    with app.app_context():
        from . import routes, models
        app.register_blueprint(routes.bp)
        db.create_all()

    return app
