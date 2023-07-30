from init import db, ma
from marshmallow import fields


class Status(db.Model):
    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    offer_status = db.Column(db.String(100), nullable=False)

    # The db.relationship() function is used to create a relationship between the Job model and the Company model.
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))

    # The back_populates argument is used to create a relationship between the Job model and the Company model.
    job = db.relationship("Job", back_populates="statuses")


class StatusSchema(ma.Schema):
    job = fields.Nested("JobSchema", only=["id", "title"])

    class Meta:
        fields = ("id", "offer_status", "job_id")
        ordered = True  # this line is used to order the fields in the schema.


# The schemas are used to serialize the data.
status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)
