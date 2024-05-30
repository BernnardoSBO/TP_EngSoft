from app import db
from marshmallow import Schema, fields
import json
from .UserModel import Users


class Products(db.Model):
    __tablename__ = "products"

    pid         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price       = db.Column(db.Float, nullable=False)
    stock       = db.Column(db.Integer, nullable=False)
    created_at  = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    updated_at  = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    vendor_id   = db.Column(db.Integer, db.ForeignKey('users.uid'), nullable=False)
    
    def __repr__(self):
        return f"""Product ID: {self.pid}
                   Name: {self.name}
                   Description: {self.description[:15]}...
                   Price: {self.price}
                   Stock: {self.stock}
                   Created at: {self.created_at}
                   Updated at: {self.updated_at}
                   Vendor: {Users.getUserById(self.vendor_id)}"""
                   
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
                   
class ProductSchema(Schema):
    pid         = fields.Integer()
    name        = fields.String()
    description = fields.String()
    price       = fields.Integer()
    stock       = fields.Integer()
    created_at  = fields.DateTime()
    updated_at  = fields.DateTime()
    vendor_id   = fields.Integer()