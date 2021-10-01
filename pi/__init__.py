from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Não tão secreta por agora'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pi.db'
db = SQLAlchemy(app)

from pi import routes