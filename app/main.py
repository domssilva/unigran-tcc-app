from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
DEBUG = os.getenv('DEBUG')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Routes
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=os.getenv('DEBUG', DEBUG), port=5001)
