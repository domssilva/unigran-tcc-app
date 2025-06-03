from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.application import Application
from services.application_service import create_application

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/dashboard')
@login_required
def dashboard():
    user_id = current_user.id
    apps = Application.query.filter_by(user_id=user_id).all()
    total_apps = len(apps)
    total_vulns = sum(app.vulnerabilities_count for app in apps)
    return render_template('dashboard.html', total_apps=total_apps, total_vulns=total_vulns)

@protected_bp.route('/me')
@login_required
def me():
    return render_template('profile.html')

@protected_bp.route('/apps', methods=['GET'])
@login_required
def apps():
    apps = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('apps.html', apps=apps)

@protected_bp.route('/apps/register', methods=['GET', 'POST'])
@login_required
def register_application():
    if request.method == 'POST':
        name = request.form['name']
        version = request.form.get('version', '')
        create_application(name, version, current_user.id)
        return redirect(url_for('protected.apps'))

    return render_template('apps_register.html')