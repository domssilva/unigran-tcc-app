from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user
from models.application import Application

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@protected_bp.route('/me')
@login_required
def me():
    return jsonify({
        'id': current_user.id,
        'name': current_user.name,
        'email': current_user.email
    })

@protected_bp.route('/apps', methods=['GET'])
@login_required
def apps():
    apps = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('apps.html', apps=apps)