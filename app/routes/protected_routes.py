from flask import Blueprint, render_template
from flask_login import login_required, current_user

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)