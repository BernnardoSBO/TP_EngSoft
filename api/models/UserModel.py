from app import db, bcrypt
from marshmallow import Schema, fields
import json


class Users(db.Model):
    __tablename__ = "users"
    
    uid      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email    = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name     = db.Column(db.String, nullable=False)
    surname  = db.Column(db.String, nullable=False)
    cpf      = db.Column(db.String, nullable=False, unique=True)
    roles    = db.Column(db.Text, nullable=False) 
    
    def __repr__(self):
        return f"""<
            User: {self.email}
            Name: {self.name}
            Surname: {self.surname}
            CPF: {self.cpf}
            roles: {self.roles}
        >"""
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self):
        db.session.commit()
        
    def setPassword(self, password):
        self.password = bcrypt.generate_password_hash(password)
        
    def checkPassword(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def setRoles(self, roles):
        self.roles = json.dumps(roles)
        
    def getRoles(self):
        return json.loads(self.roles)
    
    @classmethod
    def checkCredentials(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        return user and user.checkPassword(password)
    
    @classmethod
    def getUser(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def getUserById(cls, id):
        return cls.query.filter_by(id=id).first()
    
    def registerUser(self, email, password, name, surname, cpf, role):
        user = self.getUser(email=email)

        if user is not None:
            return None
            
        user = Users(email=email, name=name, surname=surname, cpf=cpf, roles=role)
        user.setPassword(password)
        user.save()

        return user

    
    
class UserSchema(Schema):
    uid     = fields.Integer()
    email   = fields.String()
    name    = fields.String()
    surname = fields.String()
    cpf     = fields.String()
    roles   = fields.String()