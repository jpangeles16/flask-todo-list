import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# For now I'm just gonna create a class model
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    SQLALCHEMY_DATABASE_URI='sqlite:///site.db'
)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Now make sure to import all of the routes here to prevent circular imports!
from flaskr import routes
