from init import db, ma
from marshmallow import fields

# The Applicant model is used to store information about applicants.


class Applicant(db.Model):
    __tablename__ = "applicants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    applications = db.relationship(
        "Application", back_populates="applicant", cascade="all, delete")

# The ApplicantSchema class is used to serialize and deserialize the Applicant model.


class ApplicantSchema(ma.Schema):
    applications = fields.List(fields.Nested(
        "ApplicationSchema", exclude=["applicant"]))  # this line is used to nest the application data in the applicant data.

    class Meta:
        fields = ("id", "name", "email", "password",
                  "is_admin", "applications")
        ordered = True  # this line is used to order the fields in the schema.


# this is used when we want to return a single applicant and excludes the password
applicant_schema = ApplicantSchema(exclude=["password"])
# this is used when we want to return multiple applicants and excludes the password
applicants_schema = ApplicantSchema(many=True, exclude=["password"])
