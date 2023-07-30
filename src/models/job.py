from init import db, ma


class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.Date)

    # The db.relationship() function is used to create a relationship between the Job model and the Company model.
    company_id = db.Column(db.Integer, db.ForeignKey(
        "companies.id"), nullable=False)

    company = db.relationship("Company", back_populates="jobs")


class JobSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "date_posted", "company_id")
