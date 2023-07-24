from flask import Blueprint
from init import db, bcrypt
from models.applicant import Applicant


# The db.commands blueprint is used to create the database tables and to drop the database tables.
db_commands = Blueprint("db", __name__)

# The db_commands.cli.command("create") decorator creates a command called create that can be run from the command line.


@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

 # The db_commands.cli.command("drop") decorator creates a command called drop that can be run from the command line.


@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted")

 # The db_commands.cli.command("seed") decorator creates a command called seed that can be run from the command line.


@db_commands.cli.command("seed")
def seed_db():
    applicants = [
        Applicant(name="admin", email="admin@admin.com",
                  password=bcrypt.generate_password_hash('123456').decode('utf-8'), is_admin=True),
        Applicant(name="John Smith", email="John@email.com",
                  password=(bcrypt.generate_password_hash('user1pw').decode('utf-8')))
    ]

    # The db.session.add_all(applicants) adds the applicants to the database session.
    db.session.add_all(applicants)
    # The db.session.commit() commits the changes to the database.
    db.session.commit()

    print("Tables seeded")