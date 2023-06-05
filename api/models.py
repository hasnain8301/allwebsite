from api import db, bcrypt
from datetime import datetime


# User Table 
class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    full_name = db.Column(db.String(length=15), nullable=False)
    email = db.Column(db.String(length=100), nullable=False, unique=True)
    password = db.Column(db.String(length=30), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    is_staff = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)


    # query returns instance like this
    def __repr__(self):
        return f'Name: {self.full_name} | Email: {self.email}'
    

    @property
    def hashed_password(self):
        return self.hashed_password
    
    # Create a setter to #hash the password
    @hashed_password.setter
    def hashed_password(self, password_to_hash):
        self.password = bcrypt.generate_password_hash(password_to_hash).decode('utf-8')

    # method to check the password hash
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
    

class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    project_name = db.Column(db.String(length=100), nullable=False)
    project_url = db.Column(db.String(length=255), nullable=False)
    project_type = db.Column(db.String(length=20), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow()) 
    last_deployed = db.Column(db.DateTime()) 
    project_status = db.Column(db.String(length=20), default='New Project')

    # query returns instance like this
    def __repr__(self):
        return f'Project Name: {self.project_name} | Project URL: {self.project_url} | Project Status: {self.project_status}'
    
