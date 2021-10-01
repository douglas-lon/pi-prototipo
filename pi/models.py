from datetime import datetime
from pi import db

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    materia = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    senha = db.Column(db.String(30), nullable=False)


class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)