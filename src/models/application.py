from init import db, ma
from marshmallow import fields

# Model for the job applications


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    date_applied = db.Column(db.Date, nullable=False)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=False)
    applicant_id = db.Column(db.Integer, db.ForeignKey(
        "applicants.id"), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey(
        "statuses.id"), nullable=False)

    # The back_populates argument is used to create a relationship between the Job, Applicant, and Status model with the application model.
    job = db.relationship("Job", back_populates="applications")
    applicant = db.relationship("Applicant", back_populates="applications")
    status = db.relationship("Status", back_populates="applications")


class ApplicationSchema(ma.Schema):  # Schema for serializing the application data
    job = fields.Nested("JobSchema", only=["title"])
    applicant = fields.Nested("ApplicantSchema", only=["name", "email"])
    status = fields.Nested("StatusSchema", only=["offer_status"])

    class Meta:
        # The fields are used to specify the fields that will be serialized.
        fields = ("id", "date_applied", "job", "applicant", "status")
        ordered = True  # this line is used to order the fields in the schema.


# The schemas are used to serialize the data.
application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)
