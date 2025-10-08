from flask import Blueprint, render_template, session, redirect, url_for, flash
from extensions import db
from models.user_model import User
from models.application_model import Application  # make sure this file exists and model name matches

def get_application_status():
    """Returns the tenant's application status based on their session email."""
    if 'userid' not in session:
        return None

    user = User.query.get(session['userid'])
    if not user:
        return None

    application = Application.query.filter_by(email=user.email).first()
    return application.status if application else 'Pending'

tenant_bp = Blueprint('tenant_bp', __name__, template_folder='../templates/tenant', static_folder='../static')

@tenant_bp.route('/dashboard')
def dashboard():
    if 'userid' not in session:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth_bp.login'))

    user = User.query.get(session['userid'])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('auth_bp.login'))

    status = get_application_status()

    return render_template('tenant/Dashboard.html', fullname=user.fullname, application_status=status)


@tenant_bp.route('/bills')
def bills():
    return render_template('tenant/Bills.html', application_status=get_application_status())


@tenant_bp.route('/payment')
def payment():
    return render_template('tenant/Payment.html', application_status=get_application_status())


@tenant_bp.route('/contract')
def contract():
    return render_template('tenant/Contract.html', application_status=get_application_status())


@tenant_bp.route('/support')
def support():
    return render_template('tenant/Support.html', application_status=get_application_status())


@tenant_bp.route('/browse_units')
def browse_units():
    return render_template('tenant/browse_units.html', application_status=get_application_status())
