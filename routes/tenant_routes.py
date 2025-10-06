from flask import Blueprint, render_template

tenant_bp = Blueprint('tenant_bp', __name__)

@tenant_bp.route('/dashboard')
def dashboard():
    return render_template('tenant/Dashboard.html')

@tenant_bp.route('/bills')
def bills():
    return render_template('tenant/Bills.html')

@tenant_bp.route('/payment')
def payment():
    return render_template('tenant/Payment.html')

@tenant_bp.route('/contract')
def contract():
    return render_template('tenant/Contract.html')

@tenant_bp.route('/support')
def support():
    return render_template('tenant/Support.html')
