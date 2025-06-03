from services.application_service import create_application
from models.user import User
from models.application import Application
from models import db

def test_create_application(app):
    with app.app_context():
        user = User(name="Test", email="a@b.com")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        app_created = create_application("App Test", "1.0", user.id)

        assert isinstance(app_created, Application)
        assert app_created.name == "App Test"
        assert app_created.user_id == user.id