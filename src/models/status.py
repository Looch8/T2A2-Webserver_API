from init import db, ma


class Status(db.Model):
    __tablename__ = "statuses"

    id = db.Column(db.Integer, primary_key=True)
    offer_status = db.Column(db.String(100), nullable=False)

    # The db.relationship() function is used to create a relationship between the Job model and the Company model.
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))


class StatusSchema(ma.Schema):
    class Meta:
        fields = ("id", "offer_status", "job_id")
