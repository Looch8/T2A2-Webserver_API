from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Initialise SQLAlchemy for database management
db = SQLAlchemy()

# Initialise Marshmallow for object serialization/deserialization
ma = Marshmallow()

# Initialise Bcrypt for password hashing and verification
bcrypt = Bcrypt()

# Initialise JWTManager for JSON Web Token management and handling
jwt = JWTManager()
