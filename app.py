from flask import Flask
from config import SQLALCHEMY_TRACK_MODIFICATIONS
from extensions import db
from dotenv import load_dotenv
import os

def create_app():
    # ✅ Load environment variables from .env file
    load_dotenv()

    app = Flask(__name__)

    # ✅ Securely load credentials from .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # ✅ Initialize db with app
    db.init_app(app)

    # Import models AFTER initializing db
    from models.user_model import User

    # ✅ Register blueprints
    from routes.landing_routes import landing_bp
    from routes.auth_routes import auth_bp
    from routes.tenant_routes import tenant_bp
    from routes.owner_routes import admin_bp

    app.register_blueprint(landing_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tenant_bp, url_prefix='/tenant')
    app.register_blueprint(admin_bp, url_prefix='/owner')

    # ✅ Optional: List all routes (for debugging)
    @app.route('/list_routes')
    def list_routes():
        import urllib
        output = []
        for rule in app.url_map.iter_rules():
            methods = ','.join(rule.methods)
            line = urllib.parse.unquote(f"{rule.endpoint:30s} {methods:20s} {rule}")
            output.append(line)
        return "<br>".join(sorted(output))

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # ✅ Create all tables if not exist
        db.create_all()
    app.run(debug=True)
