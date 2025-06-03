# unigran-tcc-app

project description TBD

## 🛠 Setup Environment Variables

1. **Create a `.env` file** in the project root (same folder as `app.py`):  
```bash
touch /app/.env  # Linux/Mac
type nul > \app\.env  # Windows
```

 .env example:
 ```
# .env
SECRET_KEY=your-random-secret-key
DATABASE_URL=sqlite:///app.db      # SQLite file path
 ```

🚫**Warning** - Never commit the .env to the git repo!
Ensure that .env is in the `.gitignore` file!

2. Installing dependencies
pip install -r requirements.txt

## Running Project
```bash
cd /app
python main.py
```

## DB 

Limpando o banco de dados:
1. `rm instance/app.db`
1. `rm -rf migrations/`


Iniciar banco de dados:
1. criar db:
`flask --app main:app db init`

2. gerar as migrações com todos os models:
`flask --app main:app db migrate -m "init schema"`

3. aplicar a migração
`flask --app main:app db upgrade`

---

# Doc API

Registrando usuario

```bash
curl -X POST localhost:5001/api/register -H "Content-Type: application/json" --data '{"name": "fulano", "email": "fulano@gmail.com", "password":"123456"}'
```

# Rodando Testes
`pytest tests/`