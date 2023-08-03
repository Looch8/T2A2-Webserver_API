from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models.application import Application, application_schema
from models.job import Job

applications_bp = Blueprint(
    "applications", __name__)

# CRUD functionality for the Application model


# Create Application Route
@applications_bp.route('/', methods=["POST"])
@jwt_required()
def create_application(job_id):

    # Creates a new application for a job. Retrieves JSON data from the request body and checks if the job exits, if it does, it creates a new application model instance and adds it to the database.
    body_data = request.get_json()
    stmt = db.select(Job).where(Job.id == job_id)
    job = db.session.scalar(stmt)
    if job:
        # Convert the date_applied string to a date object
        date_applied = datetime.strptime(
            body_data.get("date_applied"), "%Y-%m-%d").date()

        # Status ID is provided in the request data
        status_id = body_data.get("status_id")
        if status_id is None:
            return {"error": "Status ID is required in the request body"}, 400

        application = Application(
            date_applied=date_applied,
            # This passes the applicant id from the JWT token.
            applicant_id=get_jwt_identity(),
            # This passes the model instance to the model relationship.
            job=job,
            status_id=status_id  # Set the status_id to the provided value

        )

        db.session.add(application)
        db.session.commit()
        return application_schema.dump(application), 201
    else:
        return {"error": f"Job not found with id {job_id}"}, 404


# Delete Application Route.
@applications_bp.route('/<int:application_id>', methods=["DELETE"])
def delete_application(job_id, application_id):
    # Deletes an application from the database. Checks if the application exists, if it does, it deletes it from the database.
    stmt = db.select(Application).where(
        Application.id == application_id)
    application = db.session.scalar(stmt)
    if application:
        db.session.delete(application)
        db.session.commit()
        return {"message": f"Application with id {application_id} has been deleted"}
    else:
        return {"error": f"Application not found with id {application_id}"}, 404


# Update Application Route
@applications_bp.route('/<int:application_id>', methods=["PUT", "PATCH"])
# Update an application in the database. Checks if the application exists, if it does, it updates it in the database.
@jwt_required()
def update_application(job_id, application_id):
    body_data = request.get_json()
    stmt = db.select(Application).where(Application.id == application_id)
    application = db.session.scalar(stmt)
    if application:
        application.date_applied = body_data.get(
            "date_applied") or application.date_applied
        db.session.commit()
        return application_schema.dump(application)
    else:
        return {"error": f"Application not found with id {application_id}"}, 404
