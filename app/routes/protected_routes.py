from flask import Blueprint, make_response, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from models.application import Application
from models.vulnerability import Vulnerability
from services.application_service import create_application, update_application
from services.vulnerability_service import create_vulnerability, update_vulnerability, get_vulnerability_stats
from services.report_service import generate_csv_for_user

protected_bp = Blueprint('protected', __name__)


@protected_bp.route('/dashboard')
@login_required
def dashboard():
    stats = get_vulnerability_stats(current_user.id)

    total_apps = Application.query.filter_by(user_id=current_user.id).count()
    total_vulns = sum(stats['status'].values())

    return render_template("dashboard.html",
        current_user=current_user,
        total_apps=total_apps,
        total_vulns=total_vulns,
        vuln_status=stats['status'],
        vuln_severity=stats['severity']
    )


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


@protected_bp.route('/app/<int:id>', methods=['GET'])
@login_required
def app_detail(id):
    app = Application.query.filter_by(
        id=id, user_id=current_user.id).first_or_404()
    vulnerabilities = Vulnerability.query.filter_by(
        application_id=app.id).all()
    return render_template('app_detail.html', app=app, vulnerabilities=vulnerabilities)


@protected_bp.route('/app/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(id):
    app = Application.query.filter_by(
        id=id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        name = request.form['name']
        version = request.form.get('version', '')
        update_application(app, name, version)
        return redirect(url_for('protected.app_detail', id=app.id))
    return render_template('application_edit.html', app=app)


@protected_bp.route('/app/<int:app_id>/vulns/new', methods=['GET', 'POST'])
@login_required
def register_vulnerability(app_id):
    app = Application.query.filter_by(
        id=app_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        description = request.form['description']
        severity = request.form.get('severity', 'média')
        status = request.form.get('status', 'aberto')
        create_vulnerability(description, severity, status, app)
        return redirect(url_for('protected.app_detail', id=app.id))
    return render_template('vulnerability_register.html', app=app)


@protected_bp.route('/app/<int:app_id>/vuln/<int:vuln_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_vulnerability(app_id, vuln_id):
    app = Application.query.filter_by(
        id=app_id, user_id=current_user.id).first_or_404()
    vuln = Vulnerability.query.filter_by(
        id=vuln_id, application_id=app.id).first_or_404()

    if request.method == 'POST':
        description = request.form['description']
        severity = request.form.get('severity', 'média')
        status = request.form.get('status', 'aberto')
        update_vulnerability(vuln, description, severity, status)
        return redirect(url_for('protected.app_detail', id=app.id))
    return render_template('vulnerability_edit.html', app=app, vuln=vuln)


@protected_bp.route('/export-all')
@login_required
def export_all_vulnerabilities():
    csv_data = generate_csv_for_user(current_user.id)
    output = make_response(csv_data)
    output.headers["Content-Disposition"] = "attachment; filename=relatorio_vulnerabilidades.csv"
    output.headers["Content-type"] = "text/csv"
    return output