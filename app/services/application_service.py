from models.application import Application
from models import db

def create_application(name, version, user_id):
    app = Application(name=name, version=version, user_id=user_id)
    db.session.add(app)
    db.session.commit()
    return app

def update_application(app, name, version):
    app.name = name
    app.version = version
    db.session.commit()
    return app

def delete_application(app):
    for vuln in app.vulnerabilities:
        db.session.delete(vuln)

    db.session.delete(app)
    db.session.commit()