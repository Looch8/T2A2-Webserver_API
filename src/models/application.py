from init import db, ma


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    date_applied = db.Column(db.Date, nullable=False)

    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))
    applicant_id = db.Column(db.Integer, db.ForeignKey("applicants.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("statuses.id"))


class ApplicationSchema(ma.Schema):
    class Meta:
        fields = ("id", "date_applied", "job_id", "applicant_id", "status_id")
