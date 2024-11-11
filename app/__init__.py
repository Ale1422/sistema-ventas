from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config

login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    login_manager.init_app(app)
    login_manager.login_view = "login"

    db.init_app(app)
    migrate.init_app(app, db)    

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .public import public_bp
    app.register_blueprint(public_bp)

    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .empleado import empleado_bp
    app.register_blueprint(empleado_bp)

    return app