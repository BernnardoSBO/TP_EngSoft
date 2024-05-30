from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user
from models.ProductModel import Products, ProductSchema
from token_handler import check_access    
products_bp = Blueprint("products", __name__, url_prefix="/products")


@products_bp.route("/", methods=["GET"])
@check_access(["admin"])
def get_products():
    products = Products.query.all()

    result = ProductSchema().dump(products, many=True)

    return jsonify({"products": result}), 200

@products_bp.route("/page", methods=["GET"])
@check_access(["admin", "vendor", "client"])
def get_products_page():
    
    page = request.json.get("page", 1)
    per_page = request.json.get("per_page", 3)
        
    products = Products.query.paginate(page=page, per_page=per_page)

    result = ProductSchema().dump(products, many=True)
    
    return jsonify({"products": result}), 200


@products_bp.route("/<int:pid>", methods=["GET"])
@check_access(["admin", "vendor", "client"])
def get_product(pid):
    product = Products.query.filter_by(pid=pid).first()
    
    if not product:
        return jsonify({"msg": "Product not found", "status": 404}), 404
    

    result = ProductSchema().dump(product)

    return jsonify({"product": result}), 200

@products_bp.route("/", methods=["POST"])
@check_access(["vendor"])
def create_product():
    name = request.json.get("name")
    description = request.json.get("description")
    price = request.json.get("price")
    stock = request.json.get("stock")
    vendor_id = current_user.uid

    product = Products(
        name=name,
        description=description,
        price=price,
        stock=stock,
        vendor_id=vendor_id,
    )
    
    product.save()
    
    return jsonify({"msg": "Added product", "status": 200})

@products_bp.route("/<int:pid>", methods=["PUT"])
@check_access(["vendor"])
def update_product(pid):
    
    product = Products.query.filter_by(pid=pid).first()
    
    if (product == None):
        return jsonify({"msg": "Product not found", "status": 404}), 404

    if (product.vendor_id != current_user.uid and "admin" not in current_user.roles):
        return jsonify({"msg": "Vendor can't change this product", "status": 401}), 401    
    
    product.name = request.json.get("name", product.name)
    product.description = request.json.get("description", product.description)
    product.price = request.json.get("price", product.price)
    product.stock = request.json.get("stock", product.stock)
    
    product.update()
    
    return jsonify({"msg": "Updated product", "status": 200})

@products_bp.route("/<int:pid>", methods=["DELETE"])
@check_access(["vendor", "admin"])
def delete_product(pid):
    product = Products.query.filter_by(pid=pid).first()
    
    if (product == None):
        return jsonify({"msg": "Product not found", "status": 404}), 404

    print(current_user.getRoles())

    if (product.vendor_id != current_user.uid and "admin" not in current_user.getRoles()):
        return jsonify({"msg": "Vendor can't delete this product", "status": 401}), 401    
    
    product.delete()
    
    return jsonify({"msg": "Deleted product", "status": 200})