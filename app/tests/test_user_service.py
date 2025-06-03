from models import db
from services.user_service import create_user
from models.user import User

def test_create_user_success(app):
    with app.app_context():
        user, error = create_user("Alice", "alice@example.com", "secure123")

        assert error is None
        assert user is not None
        assert user.name == "Alice"
        assert user.email == "alice@example.com"
        assert user.check_password("secure123")

def test_create_user_missing_fields(app):
    with app.app_context():
        user, error = create_user("", "test@example.com", "")
        assert user is None
        assert error == "Missing required fields"

def test_create_user_already_exists(app):
    with app.app_context():
        # Cria usuário manualmente
        existing = User(name="Bob", email="bob@example.com")
        existing.set_password("123")
        db.session.add(existing)
        db.session.commit()

        user, error = create_user("Bob", "bob@example.com", "newpass")
        assert user is None
        assert error == "User already exists"