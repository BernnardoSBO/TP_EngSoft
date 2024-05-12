
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, current_user
from functools import wraps
from enum import Enum
from models.UserModel import Users


def error_handler(jwt):
    """This function sets up the error handler for flask_jwt
    
    Keyword arguments:
    jwt -- The instance of JWTManager()
    """
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_callback):
        return jsonify({"message:":"token expired", "error":"token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message:":"Token verification failed", "error":"invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message:":"Request doesn't contain an access token", "error":"authorization_required"}), 401
    
    
def access_handler(jwt):
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        user = Users.query.filter_by(uid=identity).first()
        
        if user.role == 1:
            return {"is_admin": True}
        else:
            return {"is_admin": False}
            
def check_access():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # jwt_required()
            verify_jwt_in_request()

            # check if current_user is admin with it's jwt
            is_admin = get_jwt().get('is_admin')
            
            if is_admin:
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Admin token required"}), 401
        return decorator
    return wrapper

