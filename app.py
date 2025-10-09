from flask import Flask, jsonify, make_response
from config import SQLALCHEMY_TRACK_MODIFICATIONS
from extensions import db
from dotenv import load_dotenv
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import pymysql
import os

def create_app():
    # ✅ Load environment variables
    load_dotenv()

    app = Flask(__name__)

    # ✅ SQLAlchemy (main ORM database)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'supersecretkey')

    # ✅ Initialize db
    db.init_app(app)

    # ✅ Import models AFTER db init
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

    # ✅ Additional: Connect to MySQL (FreeSQLDatabase.com)
    mysql_conn_settings = {
        'host': os.getenv('DB_HOST', 'sql12.freesqldatabase.com'),
        'user': os.getenv('DB_USER', 'sql12801582'),
        'password': os.getenv('DB_PASS', 'IvHCGAvMHy'),
        'database': os.getenv('DB_NAME', 'sql12801582'),
        'port': 3306
    }

    # -------------------- NEW ROUTES -------------------- #
    @app.route('/api/users', methods=['GET'])
    def get_users():
        """Return all users from FreeSQLDatabase.com"""
        try:
            conn = pymysql.connect(**mysql_conn_settings)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM Users")
            users = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(users)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/receipt/<int:order_id>', methods=['GET'])
    def generate_receipt(order_id):
        """Generate a PDF receipt from FreeSQLDatabase.com"""
        try:
            conn = pymysql.connect(**mysql_conn_settings)
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("""
                SELECT o.OrderId, o.Date, o.TotalAmount, 
                       u.FullName, u.Email,
                       p.PaymentMethod, p.PaymentDate
                FROM Orders o
                JOIN Users u ON o.UserId = u.UserId
                LEFT JOIN Payments p ON o.OrderId = p.OrderId
                WHERE o.OrderId = %s
            """, (order_id,))
            order = cursor.fetchone()

            if not order:
                return jsonify({"error": "Order not found"}), 404

            # ✅ Generate PDF in memory
            pdf_buffer = BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=A4)

            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 800, "Receipt")
            c.setFont("Helvetica", 12)
            c.drawString(50, 780, f"Order ID: {order['OrderId']}")
            c.drawString(50, 765, f"Customer: {order['FullName']}")
            c.drawString(50, 750, f"Email: {order['Email']}")
            c.drawString(50, 735, f"Order Date: {order['Date']}")
            c.drawString(50, 720, f"Payment Method: {order['PaymentMethod'] or 'N/A'}")
            c.drawString(50, 705, f"Payment Date: {order['PaymentDate'] or 'Pending'}")
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, 670, f"Total Amount: ₱{order['TotalAmount']:.2f}")
            c.showPage()
            c.save()

            pdf_buffer.seek(0)
            response = make_response(pdf_buffer.read())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'inline; filename=receipt_{order_id}.pdf'
            return response

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if conn:
                conn.close()

    # ----------------------------------------------------- #

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
