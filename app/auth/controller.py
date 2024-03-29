from app.models import Users
from app.auth.serializer import UsersSchema
from app.auth import auth_bp
from app import db, login as login_manager
from flask import jsonify, Response, request, make_response, abort
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import json

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))

@login_manager.unauthorized_handler
def unauthorized():
    abort(403, 'Not logged in')

@auth_bp.route('/protected')
@login_required
def protected():
    return jsonify({
        "id" : current_user.id,
        "username" : current_user.username
    })

# Register
@auth_bp.route('/user/register', methods = ['POST'])
def registerUser():
    """
    Create a new user
    """
    if request.data:
        data = json.loads(request.data)

    elif request.form:
        data = request.form

    # --- Validation
    username = data.get('username')
    full_name = data.get('full_name')
    password = data.get('password')
    email = data.get('email')
    if not (username and password and email and full_name):
        abort(400, 'All fields not provided')
    
     # --- check if the username exists already
    if Users.query.filter_by(username=username).first() is not None:
        abort(400, "Username already exists")
    
    # --- check if the email exists already
    if Users.query.filter_by(email=email).first() is not None:
        abort(400, "Email already exists")

    # --- Hash password
    data['password'] = generate_password_hash(password)

    # --- Add user to DB
    try:
        user = Users(**data)
        db.session.add(user)
        db.session.commit()
        response = {
            "status" : "user registered"
        }
    except Exception as e:
        abort(500, str(e))
    
    return make_response(jsonify(response), 201)

# Log In
@auth_bp.route('/user/login', methods = ['POST'])
def loginUser():
    """
    Login a user
    """
    data = json.loads(request.data)

    username = data.get('username')
    password = data.get('password')

    if not (username and password):
        abort(401, 'Required credentials not provided')

    registered_user = Users.query.filter_by(username=username).first()
    if not registered_user:
        print('1')
        abort(400, 'Incorrect username or password')

    if not check_password_hash(registered_user.password, password):
        print('2')
        abort(400, 'Incorrect username or password')

    login_user(registered_user)
    user = UsersSchema().dump(registered_user).data
    response = {
        "status" : "logged in",
        "user" : user
    }

    return make_response(jsonify(response), 200)

# User Update
# @login_required
@auth_bp.route('/user/<int:userId>/update', methods = ['PUT'])
def updateUser(userId):
    """
    Update a user's details
    """
    data = json.loads(request.data)

    user = Users.query.get(userId)
    if not user:
        abort(400, f"User with ID {userId} not found")
    
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # -- Check for existing username and email and identity
    existing_username = Users.query.filter_by(username=username).first()
    existing_email = Users.query.filter_by(email=email).first()

    if existing_username and (existing_username.username == user.username):
        abort(400, f'Username {username} already exists')
    if existing_email and (existing_email.email == user.email):
        abort(400, f'Email {email} already exists')
    
    if password:
        data['password'] = generate_password_hash(password)

    for key in data:
        setattr(user, key, data[key])
        
    try:
        db.session.add(user)
        db.session.commit()
        response = {
            "status" : "User info updated"
        }
    except Exception as e:
        abort(500, str(e))

    return make_response(jsonify(response), 200)

# Logout
@auth_bp.route('/user/logout', methods = ['GET'])
@login_required
def logoutUser():
    user = current_user.username
    logout_user()

    response = {
        "status" : "logged out"
    }

    return make_response(jsonify(response), 200)
