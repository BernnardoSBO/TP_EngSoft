from app import db, bcrypt
from marshmallow import Schema, fields


class Users(db.Model):
    __tablename__ = "users"
    
    uid      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email    = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    name     = db.Column(db.String, nullable=False)
    surname  = db.Column(db.String, nullable=False)
    cpf      = db.Column(db.String, nullable=False, unique=True)
    role     = db.Column(db.String, nullable=False) 
    
    def __repr__(self):
        return f"""<
            User: {self.email}
            Name: {self.name}
            Surname: {self.surname}
            CPF: {self.cpf}
            role: {self.role}
        >"""
        
    def save(self):

        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def setPassword(self, password):
        self.password = bcrypt.generate_password_hash(password)
        
    def checkPassword(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    @classmethod
    def checkCredentials(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        return user and user.checkPassword(password)
    
    @classmethod
    def getUser(cls, email):
        return cls.query.filter_by(email=email).first()
    
class UserSchema(Schema):
    uid = fields.Integer()
    email = fields.String()
    name = fields.String()
    surname = fields.String()
    cpf = fields.String()
    role = fields.String()