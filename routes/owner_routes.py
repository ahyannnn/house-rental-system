from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/owner')
def dashboard():
    return render_template('owner/dashboard.html')

@admin_bp.route('/tenants')
def tenants():
    return render_template('owner/tenants.html')

@admin_bp.route('/units')
def units():
    return render_template('owner/units.html')

@admin_bp.route('/transactions')
def transactions():
    return render_template('owner/transactions.html')

@admin_bp.route('/billing')
def billing():
    return render_template('owner/billing.html')

@admin_bp.route('/notification')
def notification():
    return render_template('owner/notification.html')


@admin_bp.route('/user_management')
def user_management():
    return render_template('owner/usermanagement.html')

