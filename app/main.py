from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from models import db

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DEBUG = os.getenv('DEBUG')

# Importa o objeto db do pacote models/
db.init_app(app)
from models.user import User
migrate = Migrate(app, db)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', DEBUG), port=5001)
