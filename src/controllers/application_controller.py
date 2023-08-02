from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from models.application import Application, application_schema
from models.job import Job

applications_bp = Blueprint(
    "applications", __name__)

# CRUD functionality for the Application model


# This route is used to create an application for a job.
@applications_bp.route('/', methods=["POST"])
@jwt_required()
def create_application(job_id):
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


# This route is used to delete an application from the database.
@applications_bp.route('/<int:application_id>', methods=["DELETE"])
def delete_application(job_id, application_id):
    stmt = db.select(Application).where(
        Application.id == application_id)
    application = db.session.scalar(stmt)
    if application:
        db.session.delete(application)
        db.session.commit()
        return {"message": f"Application with id {application_id} has been deleted"}
    else:
        return {"error": f"Application not found with id {application_id}"}, 404


# This route is used to update an application in the database.
@applications_bp.route('/<int:application_id>', methods=["PUT", "PATCH"])
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
