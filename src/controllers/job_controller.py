from flask import Blueprint, request
from init import db
from models.job import Job, jobs_schema, job_schema
from models.company import Company, company_schema, companies_schema
from models.applicant import Applicant
from datetime import datetime, date
from flask_jwt_extended import get_jwt_identity, jwt_required
from controllers.application_controller import applications_bp
import functools

# CRUD functionality for the Job model

# Blueprint for the job routes
jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')
jobs_bp.register_blueprint(
    applications_bp, url_prefix='/<int:job_id>/applications')


# decorator function to check if the applicant is an admin, and therefore authorised to perform certain actions.
def authorise_as_admin(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        applicant_id = get_jwt_identity()
        stmt = db.select(Applicant).where(Applicant.id == applicant_id)
        applicant = db.session.scalar(stmt)
        if applicant.is_admin:
            return fn(*args, **kwargs)
        else:
            return {"error": "You are not authorised to perform this action"}, 403

    return wrapper


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
@jwt_required()
@authorise_as_admin
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
