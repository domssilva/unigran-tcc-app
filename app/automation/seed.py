import sys
import os
from faker import Faker
from random import choice
from datetime import datetime, timedelta
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from models import db
from models.user import User
from models.application import Application
from models.vulnerability import Vulnerability

fake = Faker()

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Usuário de teste
        user = User(name="Usuário de Teste", email="teste@example.com")
        user.set_password("123456")
        db.session.add(user)
        db.session.commit()

        # Aplicação de exemplo
        app_model = Application(name="Sistema de Validação", version="1.0", user_id=user.id)
        db.session.add(app_model)
        db.session.commit()

        # Severidades e status possíveis
        severities = ["baixa", "média", "alta", "crítica"]
        statuses = ["aberto", "em andamento", "resolvido"]

        # Vulnerabilidades reais
        vuln_names = [
            "SQL Injection em campo de login",
            "Cross-Site Scripting (XSS) refletido",
            "Exposição de diretórios sensíveis",
            "Execução remota via upload de arquivos",
            "Bypass de autenticação por manipulação de token",
            "Injeção de comandos em parâmetro 'id'",
            "Token JWT não assinado",
            "Falha em validação de CSRF",
            "Quebra de autenticação por brute-force",
            "CORS mal configurado",
            "Exposição de chaves em JavaScript",
            "Deserialização insegura",
            "Redirecionamento aberto",
            "Uso de bibliotecas com CVEs conhecidas",
            "Endpoint sem autenticação em produção",
            "Injeção LDAP em busca de usuários",
            "Log de senha em texto plano",
            "Enumeração de usuários na tela de login",
            "Injeção XML (XXE)",
            "Execução de script via markdown",
            "Falta de rate limiting",
            "Erros internos expostos em produção",
            "Leitura de arquivos via path traversal",
            "Uso de HTTPS opcional",
            "Permissões excessivas em endpoints",
            "Upload de arquivos sem validação de tipo",
            "Sessão sem expiração",
            "Token reutilizável indefinidamente",
            "IDOR em edição de perfil",
            "Falta de controle de versão na API"
        ]

        for name in vuln_names:
            vuln = Vulnerability(
                description=name,
                severity=choice(severities),
                status=choice(statuses),
                date_discovered=fake.date_between(start_date='-90d', end_date='today'),
                application_id=app_model.id
            )
            db.session.add(vuln)

        db.session.commit()
        print("Banco de dados populado com sucesso com 1 usuário, 1 app e 30 vulnerabilidades.")

if __name__ == "__main__":
    seed()