from services.report_service import generate_csv_for_user
from models.user import User
from models.application import Application
from models.vulnerability import Vulnerability
from models import db

def test_generate_csv_for_user(app):
    with app.app_context():
        # Cria usuário e dados relacionados
        user = User(name="Carlos", email="carlos@example.com")
        user.set_password("senha123")
        db.session.add(user)
        db.session.commit()

        app_model = Application(name="App Teste", version="1.0", user_id=user.id)
        db.session.add(app_model)
        db.session.commit()

        vuln = Vulnerability(
            description="Exemplo de vulnerabilidade",
            severity="alta",
            status="aberto",
            application_id=app_model.id
        )
        db.session.add(vuln)
        db.session.commit()

        # Gera CSV
        csv_data = generate_csv_for_user(user.id)

        # Verificações
        assert isinstance(csv_data, str)
        assert "ID,Descrição,Severidade,Status,Data Descoberta" in csv_data
        assert "Exemplo de vulnerabilidade" in csv_data
        assert "alta" in csv_data
