from flask import Blueprint, jsonify, request
from flask_jwt_extended import unset_jwt_cookies, create_access_token, jwt_required, get_jwt, get_jwt_identity, current_user
from models.UserModel import Users
from app import bcrypt, db
from token_handler import check_access

from datetime import datetime, timedelta, timezone
import json


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register_user():
    email = request.json.get("email")
    password = request.json.get("password")
    name = request.json.get("name")
    surname = request.json.get("surname")
    cpf = request.json.get("cpf")
    role = 0
    
    user = Users.query.filter_by(email=email).first()
    
    if user is not None:
        return jsonify({"msg": "user already exists", "status": 409} ), 409
    
    user = Users(email=email, name=name, surname=surname, cpf=cpf, role=role)
    user.setPassword(password)
    
    user.save()
    
    return jsonify({ "msg": "Added User" , "status":200})

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "logout successful", "status": 200}), 200
    unset_jwt_cookies(response)
    return response


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"msg": "Email and password are required", "status": 400}), 400

    if not Users.checkCredentials(email=email, password=password):
        return jsonify({"msg": "Invalid credentials", "status": 401}), 401
    
    user = Users.getUser(email=email)
    is_admin = int(user.role) == 1 
    
    access_token = create_access_token(identity=user.uid, additional_claims={"is_admin": is_admin})
    
    return jsonify({"msg": "Successful login",
                    "access_token": access_token,
                    "status": 200}), 200
    
@auth_bp.route('/whoami', methods=['GET'])
@jwt_required()
@check_access()
def whoami():
    claims = get_jwt()
    
    # return jsonify({"claims": claims})
    if claims.get('is_admin'):
        identity = get_jwt_identity()
        return jsonify({ "identity": identity})
    
    return jsonify({"msg": "not admin"})
    
    # print(get_jwt())
    # if claims.get('is_admin'):
    #     identity = get_jwt_identity()
        
    # else:
    #     return jsonify({"msg": "not admin"})
    


    
@auth_bp.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        return response
        

