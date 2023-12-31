from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length

# Model for the Job table


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.String(50), nullable=False)

    # The db.relationship() function is used to create a relationship between the Job model and the Company model.
    company_id = db.Column(db.Integer, db.ForeignKey(
        "companies.id"), nullable=False)

    company = db.relationship("Company", back_populates="jobs")
    applications = db.relationship(
        "Application", back_populates="job", cascade="all, delete")

    statuses = db.relationship(
        "Status", back_populates="job")


class JobSchema(ma.Schema):
    applications = fields.List(fields.Nested(
        "ApplicationSchema"), exclude=["job"])
    # this line is used to nest the company data in the job data.
    companies = fields.Nested("CompanySchema", only=[
                              "id", "name"])

    # The validation parameter is used to validate the data before it is stored in the database.
    title = fields.String(required=True, validate=Length(
        min=2, error="Title must be at least 2 characters long."))
    description = fields.String(required=True, validate=Length(
        min=10), error="Description must be at least 10 characters long.")

    class Meta:
        fields = ("id", "title", "description",
                  "date_posted", "company_id", "company.name")  # The fields are used to specify the fields that will be serialized.
        ordered = True  # this line is used to order the fields in the schema.


# The schemas are used to serialize the data.
job_schema = JobSchema()
jobs_schema = JobSchema(many=True)
