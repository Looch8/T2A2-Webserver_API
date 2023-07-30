from init import db, ma
from marshmallow import fields


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(100))

    jobs = db.relationship(
        "Job", back_populates="company", cascade="all, delete")


class CompanySchema(ma.Schema):
    jobs = fields.List(fields.Nested("jobSchema", exclude=["company"]))

    class Meta:
        fields = ("id", "name", "location", "website")
        ordered = True  # this line is used to order the fields in the schema.


# The schemas are used to serialize the data.
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
