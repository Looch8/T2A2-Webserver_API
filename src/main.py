from flask import Flask
import os
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.auth_controller import auth_bp
from controllers.job_controller import jobs_bp
from controllers.application_controller import applications_bp
from marshmallow.exceptions import ValidationError


def create_app():
    app = Flask(__name__)

    # This line is used to prevent the JSON responses from being sorted alphabetically so our ordered = True statement works as intended.
    app.json.sort_keys = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL")  # This is the database URL, it is in the .env file

    # This is a secret key, it is in the .env file and it is used to encrypt the JWT token
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

    # This is used to handle validation errors
    @app.errorhandler(ValidationError)
    def validation_error(error):
        # This returns the validation error message as a JSON response with a 400 status code
        return error.messages, 400

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # The app.register_blueprint() method is used to register the blueprints.
    app.register_blueprint(db_commands)
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(applications_bp)

    return app
