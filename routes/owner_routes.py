from flask import Blueprint, render_template

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/')
def dashboard():
    return render_template('owner/Dashboard.html')

@admin_bp.route('/tenants')
def tenants():
    return render_template('owner/Tenants.html')

@admin_bp.route('/units')
def units():
    return render_template('owner/Units.html')

@admin_bp.route('/billing')
def billing():
    return render_template('owner/Billing.html')

@admin_bp.route('/concern')
def concern():
    return render_template('owner/Concern.html')
