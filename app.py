from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)

    # Import blueprints
    from routes.landing_routes import landing_bp
    from routes.auth_routes import auth_bp
    from routes.tenant_routes import tenant_bp
    from routes.owner_routes import admin_bp

    # Register blueprints
    app.register_blueprint(landing_bp)                  # 👈 /
    app.register_blueprint(auth_bp, url_prefix='/auth') # /auth/login, /auth/register
    app.register_blueprint(tenant_bp, url_prefix='/tenant')
    app.register_blueprint(admin_bp, url_prefix='/owner')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
