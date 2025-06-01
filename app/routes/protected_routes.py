from flask import Blueprint, jsonify, render_template
from flask_login import login_required, current_user

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