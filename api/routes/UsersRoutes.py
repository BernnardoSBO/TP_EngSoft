from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.UserModel import Users, UserSchema

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    users = Users.query.all()
    
    result = UserSchema().dump(users, many=True)
    
    return jsonify({"users": result}), 200


@users_bp.route('/<int:uid>', methods=['GET'])
@jwt_required()
def get_user(uid):
    user = Users.query.filter_by(uid=uid).first()
    
    if not user:
        return jsonify({"msg": "user not found", "status": 404}), 404
    
    result = UserSchema().dump(user)
    
    return jsonify({"users": result}), 200


def get_pagination_params(data):
    DEFAULT_PAGE = 1
    DEFAULT_PER_PAGE = 3
    
    if data is None:
        return DEFAULT_PAGE, DEFAULT_PER_PAGE
    
    page = data.get("page", DEFAULT_PAGE)
    per_page = data.get("per_page", DEFAULT_PER_PAGE)
    
    return page, per_page


@users_bp.route('/page', methods=['GET'])
@jwt_required()
def get_users_page():
    data = request.get_json(silent=True)
    
    page, per_page = get_pagination_params(data)
    
    users = Users.query.paginate(page=page, per_page=per_page)
    
    result = UserSchema().dump(users.items, many=True)
    
    return jsonify({"users": result}), 200


@users_bp.route('/', methods=['POST'])
def create_user():
    pass

# @users_bp.route('/<int:uid>', methods=['PUT'])
# def update_user(uid):
#     pass

# @users_bp.route('/<int:uid>', methods=['DELETE'])
# def delete_user(uid):
#     pass

# @users_bp.route('/token', methods=['POST'])
# def create_token():
#     pass