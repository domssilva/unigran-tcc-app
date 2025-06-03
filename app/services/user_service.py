from models import db
from models.user import User

def create_user(name, email, password):
    if not all([name, email, password]):
        return None, "Missing required fields"

    if User.query.filter_by(email=email).first():
        return None, "User already exists"

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user, None