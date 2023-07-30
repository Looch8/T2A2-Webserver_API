from init import db, ma
from marshmallow import fields


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    date_applied = db.Column(db.Date, nullable=False)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    applicant_id = db.Column(db.Integer, db.ForeignKey("applicants.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"))

    # The back_populates argument is used to create a relationship between the Job, Applicant, and Status model and the Company model.
    job = db.relationship("Job", back_populates="applications")
    applicant = db.relationship("Applicant", back_populates="applications")
    status = db.relationship("Status", back_populates="applications")


class ApplicationSchema(ma.Schema):
    job = fields.Nested("JobSchema", only=["id", "title"])
    applicant = fields.Nested("ApplicantSchema", only=["id", "name"])
    status = fields.Nested("StatusSchema", only=["id", "offer_status"])

    class Meta:
        fields = ("id", "date_applied", "job_id", "applicant_id", "status_id")
        ordered = True  # this line is used to order the fields in the schema.


# The schemas are used to serialize the data.
application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)
