from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL")  # This is the database URL, it is in the .env file

    # This is a secret key, it is in the .env file and it is used to encrypt the JWT token
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # The app.register_blueprint() method is used to register the blueprints.
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)

    return app
