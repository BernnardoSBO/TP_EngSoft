from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from datetime import datetime, timedelta, timezone
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt_manager = JWTManager()


def create_app():
    app = Flask(__name__)
    app.instance_path = './db/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'db/db.sqlite')
    app.config['SECRET_KEY'] = 'DUMB_SECRET_KEY'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    
    # tool initialization
    db.init_app(app)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)
    
    # jwt handling
    from token_handler import error_handler
    error_handler(jwt_manager)
    
    # routes
    from routes.AuthRoutes import auth_bp
    app.register_blueprint(auth_bp)
    
    from routes.UsersRoutes import users_bp
    app.register_blueprint(users_bp)
    
    # db migration
    migrate = Migrate(app, db, directory='db/migrations')
    
    return app