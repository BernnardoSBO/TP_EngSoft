from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from models.UserModel import Users, UserSchema
from token_handler import check_access

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
@check_access(["admin"])
def get_users():
    users = Users.query.all()
    
    result = UserSchema().dump(users, many=True)
    
    return jsonify({"users": result}), 200

@users_bp.route('/<int:uid>', methods=['GET'])
@check_access(["admin", "vendor", "client"])
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
@check_access(["admin", "vendor", "client"])
def get_users_page():
    data = request.get_json(silent=True)
    
    page, per_page = get_pagination_params(data)
    
    users = Users.query.paginate(page=page, per_page=per_page)
    
    result = UserSchema().dump(users.items, many=True)
    
    return jsonify({"users": result}), 200

    
@users_bp.route('/add_role/<int:uid>', methods=['PUT'])
@check_access(["admin"])
def add_role(uid):
    user = Users.query.filter_by(uid=uid).first()
    
    if (user == None):
        return jsonify({"msg": "user not found", "status": 404}), 404
    
    user_roles = set(user.getRoles())
    print(user_roles)
    user_roles.add(request.json.get("role", None))
    
    user.setRoles(list(user_roles))
    
    user.update()
     
    return jsonify({"msg": "Updated user", "status": 200})

@users_bp.route('/remove_role/<int:uid>', methods=['PUT'])
@check_access(["admin"])
def remove_role(uid):
    user = Users.query.filter_by(uid=uid).first()
    
    if (user == None):
        return jsonify({"msg": "user not found", "status": 404}), 404
    
    remove_role = request.json.get("role")

    user_roles = set(user.getRoles())
    
    if remove_role not in user_roles:
        return jsonify({"msg": f"User doesn't have role {remove_role}", "status": 404}), 404
    
    user_roles.remove(request.json.get("role", None))
    
    user.setRoles(list(user_roles))
    
    user.update()
     
    return jsonify({"msg": "Updated user", "status": 200})


@users_bp.route('/delete_account', methods=['DELETE'])
@check_access(["admin", "client", "vendor"])
def delete_self():
    user = Users.query.filter_by(uid=current_user.uid).first()
    
    if (user == None):
        return jsonify({"msg": "user not found", "status": 404}), 404
    
    user.delete()
    
    return jsonify({"msg": "Deleted user", "status": 200})

@users_bp.route('/delete_account/<int:uid>', methods=['DELETE'])
@check_access(["admin"])
def delete_account(uid):
    user = Users.query.filter_by(uid=uid).first()
    
    if (user == None):
        return jsonify({"msg": "user not found", "status": 404}), 404
    
    user.delete()
    
    return jsonify({"msg": "Deleted user", "status": 200})
