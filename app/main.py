import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, current_user
from dotenv import load_dotenv
from models import db
from routes import auth_bp, protected_bp

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DEBUG = os.getenv('DEBUG')


# Inicializa db (sequencia de comandos importa, nao mude)
db.init_app(app)
from models.user import User
migrate = Migrate(app, db)

# gerenciamento de sessao
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Credenciais inválidas', 'danger')
            return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))

    elif request.method == 'POST':
        logout_user()
        return redirect(url_for('login_page'))

app.register_blueprint(auth_bp)
app.register_blueprint(protected_bp)

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', DEBUG), port=5001)
