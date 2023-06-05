from flask import jsonify, request, make_response
from flask.blueprints import Blueprint
from api.models import User
from api import db
import jwt
import datetime
from api import config
from api.decorator import token_required


# Create A Blueprint 
auth = Blueprint('auth', __name__, url_prefix='/auth')


# route to register new user
@auth.route('/adduser', methods=['POST'])
@token_required
def register_user(current_user):
    
    # get data from request
    data = request.get_json()

    # if data recieved create a user instance and save in database
    if data:
        create_user = User(full_name=data['full_name'], email=data['email'], hashed_password=data['password'])
        db.session.add(create_user)
        db.session.commit()

        result = {'message':'User created successfully'}
        return jsonify(result), 201
        


# route to user login and generate auth token
@auth.route('/login', methods=['POST'])
def login_user():

    # get login data from request
    auth = request.authorization

    # Check if data recieved from request
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    # fetch user from database
    user = User.query.filter_by(email=auth.username).first()

    # If User Not Exist
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    
    # Check Password Hash
    if user.check_password_correction(attempted_password=auth.password):
        # create jwt token 
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, config.SECRET_KEY, algorithm="HS256")
        # return jwt token 
        return jsonify({'auth_token' : token}), 200

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

