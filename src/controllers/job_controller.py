from flask import Blueprint, request
from init import db
from models.job import Job, jobs_schema, job_schema
from models.application import Application, application_schema, applications_schema
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required

# CRUD functionality for the Job model

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')


# This route is used to get all the jobs from the database.
@jobs_bp.route('/')
def get_all_jobs():
    stmt = db.select(Job).order_by(Job.date_posted.desc())
    jobs = db.session.scalars(stmt)
    return jobs_schema.dump(jobs)


# This route is used to get a specific job from the database.
@jobs_bp.route('/<int:id>')
def get_one_job(id):
    stmt = db.select(Job).where(Job.id == id)
    job = db.session.scalar(stmt)
    # The if/else condition is used to check if the job exists.
    if job:
        return job_schema.dump(job)
    else:
        return {"error": f"Job not found with id {id}"}, 404


# This route is used to create a job in the database.
@jobs_bp.route('/', methods=["POST"])
@jwt_required()  # This decorator is used to protect the route.
def create_job():
    body_data = request.get_json()
    # Create a new job model instance
    job = Job(
        title=body_data.get("title"),
        description=body_data.get("description"),
        date_posted=date.today(),
        company_id=get_jwt_identity()
    )

    db.session.add(job)
    db.session.commit()

    return job_schema.dump(job), 201


# This route is used to delete a job from the database.
@jobs_bp.route('/<int:id>', methods=["DELETE"])
def delete_job(id):
    stmt = db.select(Job).where(Job.id == id)
    job = db.session.scalar(stmt)
    if job:
        db.session.delete(job)
        db.session.commit()
        return {"error": f"Job with id {id} has been deleted"}
    else:
        return {"error": f"Job not found with id {id}"}, 404


# This route is used to update a job in the database.
@jobs_bp.route('/<int:id>', methods=["PUT", "PATCH"])
@jwt_required()
def update_job(id):
    body_data = request.get_json()
    stmt = db.select(Job).where(Job.id == id)
    job = db.session.scalar(stmt)
    if job:
        job.title = body_data.get("title") or job.title
        job.description = body_data.get("description") or job.description
        job.date_posted = body_data.get("date_posted") or job.date_posted
        db.session.commit()
        return job_schema.dump(job)
    else:
        return {"error": f"Job not found with id {id}"}, 404


# CRUD functionality for the Application model
# This route is used to create an application for a job.
@jobs_bp.route('/<int:job_id>/applications', methods=["POST"])
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
