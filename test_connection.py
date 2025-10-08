from app import create_app
from extensions import db
from models.user_model import User
from sqlalchemy import text  # ✅ Import text()

app = create_app()

with app.app_context():
    print("✅ Testing database connection...")

    try:
        # ✅ Use text() for raw SQL queries
        db.session.execute(text("SELECT 1"))
        print("✅ Database connected successfully!")

        # ✅ Try retrieving data from Users table
        users = User.query.all()
        if users:
            print(f"✅ Retrieved {len(users)} user(s):")
            for user in users:
                print(f" - {user.userid}: {user.fullname} ({user.email})")
        else:
            print("⚠️ No users found in the database.")

    except Exception as e:
        print("❌ Database test failed:", e)
