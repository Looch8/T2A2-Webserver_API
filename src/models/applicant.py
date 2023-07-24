from init import db, ma

# The Applicant model is used to store information about applicants.


class Applicant(db.model):
    __tablename__ = "applicants"

    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(100), nullable=False)
    email = db.column(db.String(100), nullable=False, unique=True)
    password = db.column(db.String(100), nullable=False)
    is_admin = db.column(db.Boolean, default=False)

# The ApplicantSchema class is used to serialize and deserialize the Applicant model.


class ApplicantSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin")


# this is used when we want to return a single applicant and excludes the password
applicant_schema = ApplicantSchema(exclude=["password"])
# this is used when we want to return multiple applicants and excludes the password
applicants_schema = ApplicantSchema(many=True, exclude=["password"])
