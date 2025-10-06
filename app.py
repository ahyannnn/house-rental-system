from flask import Flask
from config import SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from extensions import db  # ✅ import db from extensions

def create_app():
    app = Flask(__name__)

    # ✅ Correct MSSQL connection string
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "mssql+pyodbc://@DESKTOP-6ORQFPB\\SQLEXPRESS/TRAMS?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

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
        db.create_all()
    app.run(debug=True)
