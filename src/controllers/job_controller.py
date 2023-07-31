from flask import Blueprint, request
from init import db
from models.job import Job, jobs_schema, job_schema

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

# The get_all_jobs() function is used to get all the jobs from the database.


@jobs_bp.route('/')
def get_all_jobs():
    stmt = db.select(Job).order_by(Job.date_posted.desc())
    jobs = db.session.scalars(stmt)
    return jobs_schema.dumps(jobs)
