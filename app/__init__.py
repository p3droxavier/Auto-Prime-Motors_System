# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from app.database import db
from app.auth.routes import fake_admin
import os
 
 
def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    
    from app.database.models.funcionario import Funcionario

    @login_manager.user_loader
    def load_user(user_id):
        # Se for admin fixo
        if str(user_id) == str(fake_admin.id):
            return fake_admin
        
        # Se for funcionario do banco 
        return Funcionario.query.get(int(user_id))

    # Blueprints
    from app.auth.routes import auth_bp
    from app.dashboard.funcionario_routes import dashboard_bp
    from app.dashboard.admin_routes import admin_dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_dashboard_bp, url_prefix='/dashboard')
    # app.register_blueprint(admin_dashboard_bp, url_prefix='/admin')

    return app
