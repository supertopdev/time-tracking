from flask import Flask, jsonify, make_response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS, cross_origin

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        # TODO: Remove this log
        print("error : ", error)
        error_code = getattr(error, 'code', 500)
        error_description = getattr(error, 'name', '')
        error_message = getattr(error, 'description', '')
        return make_response(
            jsonify({'error':error_code,
            'message':error_message}), error_code
        )

    for errcode in [400, 401, 403, 404, 405, 500]:
        app.errorhandler(errcode)(render_error)

def create_app(config_class=Config):
    app = Flask(__name__)
    cors = CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.secret_key = "asdaweda"
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.main import main_bp
    app.register_blueprint(main_bp)
    register_errorhandlers(app)

    return app

from app import models