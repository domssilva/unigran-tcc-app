from services.application_service import create_application, update_application, delete_application
from models.user import User
from models.application import Application
from models.vulnerability import Vulnerability
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

def test_update_application(app):
    with app.app_context():
        # Cria usuário e aplicação
        user = User(name="Maria", email="maria@teste.com")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()

        app_model = Application(name="Nome Original", version="1.0", user_id=user.id)
        db.session.add(app_model)
        db.session.commit()

        # Atualiza a aplicação
        updated = update_application(app_model, name="App Atualizado", version="2.5")

        # Verificações
        assert updated.name == "App Atualizado"
        assert updated.version == "2.5"

        app_db = Application.query.get(app_model.id)
        assert app_db.name == "App Atualizado"
        assert app_db.version == "2.5"

def test_delete_application(app):
    with app.app_context():
        user = User(name="Teste", email="teste@app.com")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        app_model = Application(name="App Deletável", version="1.0", user_id=user.id)
        db.session.add(app_model)
        db.session.commit()

        # Adiciona 2 vulnerabilidades
        v1 = Vulnerability(description="Falha A", severity="alta", status="aberto", application_id=app_model.id)
        v2 = Vulnerability(description="Falha B", severity="média", status="resolvido", application_id=app_model.id)
        db.session.add_all([v1, v2])
        db.session.commit()

        # Verifica que tudo existe
        assert Application.query.count() == 1
        assert Vulnerability.query.count() == 2

        # Executa exclusão
        delete_application(app_model)

        assert Application.query.count() == 0
        assert Vulnerability.query.count() == 0