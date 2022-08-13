import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("USER")}:{os.environ.get("PASS")}@{os.environ.get("HOST")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB")}'
print(SQLALCHEMY_DATABASE_URI)
