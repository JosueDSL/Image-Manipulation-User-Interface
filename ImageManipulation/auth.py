from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# Hash the password for the test user
hashed_password = generate_password_hash('test')

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Error handling for the request
    if not data:
        return jsonify(message='No input data provided'), 400
    
    print(data)

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify(message='Username or password not provided'), 400
    
    if username == 'test' and check_password_hash(hashed_password, password):
        return jsonify(access_token=create_access_token(identity=username)), 200
    else:
        return jsonify(message='Invalid credentials'), 401        




# Protected endpoint that requires JWT token for access - Testing purposes
@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="You are authenticated!"), 200