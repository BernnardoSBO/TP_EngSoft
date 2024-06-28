
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
    

           
def role_handler(jwt):
    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_callback):
        identity = jwt_callback['sub']
        return Users.query.filter_by(uid=identity).one()
           
            
def check_access(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # jwt_required()
            verify_jwt_in_request()

            user_roles = current_user.getRoles()
            
            if not isinstance(user_roles, (list, set)):
                user_roles = [user_roles]

            # check if current_user has the necessary role to access the route
            if any(role in user_roles for role in roles):
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Role not authorized"}), 401
        return decorator
    return wrapper

