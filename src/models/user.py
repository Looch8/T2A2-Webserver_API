from init import db, ma


class Applicant(db.model):
    __tablename__ = "applicants"

    id = db.column(db.Integer, primary_key=True)
    name = db.column(db.String(100), nullable=False)
    email = db.column(db.String(100), nullable=False, unique=True)
    password = db.column(db.String(100), nullable=False)
    is_admin = db.column(db.Boolean, default=False)
