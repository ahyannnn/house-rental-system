from flask import Blueprint, render_template, request, redirect, url_for, flash

auth_bp = Blueprint('auth_bp', __name__, template_folder='../templates/auth', static_folder='../static')

# --- LOGIN PAGE ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Example login logic (replace with your database check)
        if email == "admin@phome.com" and password == "1234":
            flash("Login successful!", "success")
            return redirect(url_for('landing'))  # redirect to your main page
        else:
            flash("Invalid credentials", "danger")

    return render_template('auth/login.html')


# --- REGISTER PAGE ---
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            flash("Passwords do not match!", "danger")
        else:
            # TODO: Save user to DB
            flash("Account created successfully!", "success")
            return redirect(url_for('auth_bp.login'))

    return render_template('auth/register.html')
