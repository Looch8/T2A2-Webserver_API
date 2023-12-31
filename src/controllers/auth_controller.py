from flask import Blueprint, request
from init import db, bcrypt
from models.applicant import Applicant, applicant_schema, applicants_schema
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from psycopg2 import errorcodes

# Create auth blueprint and routes for authentication
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# Registration route

# Register new applicants
@auth_bp.route("/register", methods=["POST"])
def auth_register():
    try:
        body_data = request.get_json()

        # Creates a new applicant model and sets the name, email, and password attributes.
        applicant = Applicant()
        applicant.name = body_data.get("name")
        applicant.email = body_data.get("email")
        if body_data.get('password'):
            # Hashes the password using the bcrypt library and store it.
            applicant.password = bcrypt.generate_password_hash(
                body_data.get("password")).decode("utf-8")

        # adds the applicant to the database session.
        db.session.add(applicant)
        db.session.commit()
        # returns the applicant as JSON.
        return applicant_schema.dump(applicant), 201
        # 201 is the status code for successfully created
    except IntegrityError as e:
        if e.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"error": "Email already exists"}, 401
        if e.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # returns the error message and the column name that caused the error.
            return {"error": f" the {e.orig.diag.column_name} is required"}, 401
    # 401 is the status code for unauthorized

# Login Route


@auth_bp.route("/login", methods=["POST"])
# this function is used to login applicants.
def auth_login():
    body_data = request.get_json()
    # Find applicant by email
    stmt = db.select(Applicant).where(
        Applicant.email == body_data.get("email"))
    applicant = db.session.scalar(stmt)
    # If applicants exists, and password matches, create access token
    if applicant and bcrypt.check_password_hash(applicant.password, body_data.get("password")):
        token = create_access_token(identity=str(
            applicant.id), expires_delta=timedelta(days=1))
        # 200 is the status code for OK
        return {'email': applicant.email, 'token': token, 'is_admin': applicant.is_admin}, 200
    else:
        # 401 is the status code for unauthorized
        return {"error": "Invalid email or password"}, 401
