from extensions import db
from app import create_app
from models.user_model import User
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app()

with app.app_context():
    try:
        # Check if the test user already exists
        existing_user = User.query.filter_by(email="testuser@example.com").first()
        if existing_user:
            print("⚠️  Test user already exists in the database.")
        else:
            # Create a new test user
            new_user = User(
                fullname="Test User",
                email="testuser@example.com",
                phone="09123456789",
                password=generate_password_hash("password123"),
                role="tenant",
                datecreated=datetime.utcnow()   # ✅ Add creation date
            )

            # Add to database
            db.session.add(new_user)
            db.session.commit()

            print("✅ User added successfully!")
            print(f"User ID: {new_user.userid}, Name: {new_user.fullname}, Email: {new_user.email}")
            print(f"Date Created: {new_user.datecreated}")

        # Verify all users
        users = User.query.all()
        print(f"\n📋 Total users in database: {len(users)}")
        for user in users:
            print(f"- {user.userid}: {user.fullname} ({user.email}) | Created: {user.datecreated}")

    except Exception as e:
        print("❌ Error adding user:")
        print(e)
