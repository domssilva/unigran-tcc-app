import csv
from io import StringIO
from models.vulnerability import Vulnerability
from models.application import Application
from models import db

def generate_csv_for_user(user_id):
    vulns = (
        db.session.query(Vulnerability)
        .join(Application)
        .filter(Application.user_id == user_id)
        .all()
    )

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['ID', 'Descrição', 'Severidade', 'Status', 'Data Descoberta'])

    for v in vulns:
        writer.writerow([
            v.id,
            v.description,
            v.severity,
            v.status,
            v.date_discovered.strftime('%Y-%m-%d') if v.date_discovered else ''
        ])

    return si.getvalue()
