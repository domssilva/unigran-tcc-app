from models.application import Application
from models import db

def create_application(name, version, user_id):
    app = Application(name=name, version=version, user_id=user_id)
    db.session.add(app)
    db.session.commit()
    return app
