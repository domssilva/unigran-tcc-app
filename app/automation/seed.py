import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from models import db
from models.user import User
from models.application import Application
from models.vulnerability import Vulnerability

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(name='Admin', email='admin@gmail.com')
        user.set_password('123')
        db.session.add(user)
        db.session.commit()

        apps = [
            Application(name='Sistema de RH', version='1.0.0', user_id=user.id),
            Application(name='Portal Financeiro', version='2.3.1', user_id=user.id),
            Application(name='Plataforma de Pagamentos', version='0.9.5', user_id=user.id),
        ]
        db.session.add_all(apps)
        db.session.commit()

        vuln = Vulnerability(
            description='Falha de autenticação sem MFA',
            severity='alta',
            status='aberto',
            application_id=apps[0].id
        )
        db.session.add(vuln)
        apps[0].vulnerabilities_count += 1
        db.session.commit()

        print("Banco de dados populado com sucesso.")

if __name__ == '__main__':
    seed()
