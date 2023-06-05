from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# create SQLAlchemy class instance
db = SQLAlchemy()

# Bcrypt to create password hashing
bcrypt = Bcrypt()



# Define App 
def create_app(configfile="config.py"): 
    app = Flask(__name__)

    # Get configurations form 'config.py' file
    app.config.from_pyfile(configfile)

    # initiate SQLAlchemy database with app
    db.init_app(app)
    # Handel The database and Table creation
   

    # Register auth as blueprint of application
    from api.auth import auth
    app.register_blueprint(auth)

    # Register views as blueprint of application
    from api.views import views
    app.register_blueprint(views)

    return app