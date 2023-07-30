# The cli_controller.py file is used to create, seed, and drop the database tables.
from flask import Blueprint
from init import db, bcrypt
from models.applicant import Applicant
from models.job import Job
from models.application import Application
from models.company import Company
from models.status import Status

# The db.commands blueprint is used to create the database tables and to drop the database tables.
db_commands = Blueprint("db", __name__)

# The db_commands.cli.command decorators creates commands to create, seed, and drop data and can be run from the command line.


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted")


@db_commands.cli.command("seed")
def seed_db():
    companies = [
        Company(name="Google",
                location="Mountain View, CA",
                website="www.google.com"
                ),
        Company(name="Facebook",
                location="Menlo Park, CA",
                website="www.facebook.com"
                ),
        Company(name="Amazon",
                location="Seattle, WA",
                website="www.amazon.com"
                ),
    ]
    db.session.add_all(companies)
    db.session.commit()

    applicants = [
        Applicant(name="admin", email="admin@admin.com",
                  password=bcrypt.generate_password_hash('123456').decode('utf-8'), is_admin=True),
        Applicant(name="John Smith", email="John@email.com",
                  password=(bcrypt.generate_password_hash('user1pw').decode('utf-8')))
    ]
    db.session.add_all(applicants)

    jobs = [
        Job(title="Software Engineer",
            description="A software engineer is a person who applies the principles of software engineering to computer software.",
            date_posted="2021-01-01",
            company=companies[0]
            ),
        Job(title="Software Developer",
            description="A software developer is a person concerned with the development process of computer software.",
            date_posted="2022-07-09",
            company=companies[1]
            ),
        Job(title="Web Developer",
            description="A web developer is a programmer who specializes in the development of World Wide Web applications.",
            date_posted="2021-03-15",
            company=companies[2]
            ),
    ]
    db.session.add_all(jobs)
    db.session.commit()

    print("Tables seeded")
