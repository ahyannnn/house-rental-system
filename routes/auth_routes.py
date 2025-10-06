from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.user_model import User
auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/auth', static_folder='../static')

# --- LOGIN ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        print("Email entered:", email)
        print("Password entered:", password)
        print("User found:", user)
        if user:
          print("Stored hash:", user.password)
        if user and check_password_hash(user.password, password):
            # ✅ Store session
            session['userid'] = user.userid
            session['fullname'] = user.fullname
            session['role'] = user.role

            flash(f"Welcome, {user.fullname}!", "success")

            if user.role.lower() == 'tenant':
                return redirect(url_for('tenant_bp.dashboard'))
            elif user.role.lower() == 'owner':
                return redirect(url_for('admin_bp.dashboard'))
            else:
                return redirect(url_for('landing_bp.home'))

        else:
            flash("Invalid email or password.", "danger")

    return render_template('auth/login.html')


# --- REGISTER ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        # ✅ Validation
        if not fullname or not email or not phone or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for('auth_bp.register'))

        if password != confirm:
            flash("Passwords do not match!", "danger")
            return redirect(url_for('auth_bp.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for('auth_bp.register'))

        # ✅ Save new user (default role: tenant)
        hashed_password = generate_password_hash(password)
        new_user = User(fullname=fullname, email=email, phone=phone, password=hashed_password, role='Tenant', datecreated=db.func.current_timestamp())

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('auth_bp.login'))

    return render_template('auth/register.html')


# --- LOGOUT ---
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have logged out successfully.", "info")
    return redirect(url_for('landing_bp.landing_page'))
