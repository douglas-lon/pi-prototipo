from datetime import datetime
from pi import db, login_manager
from flask_login import UserMixin

# Função do flask_login necessária para ele funcionar
@login_manager.user_loader
def load_user(professor_id):
    return Professor.query.get(int(professor_id))


# Cria tabela professor, e utiliza a tabela materia para o campo materia
class Professor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    materia = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    senha = db.Column(db.String(30), nullable=False)


    def __repr__(self):
        return f"Professor('{self.nome}', '{self.email}', '{self.materia}')"


# Cria tabela materia,
class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Materia('{self.id}', '{self.nome}')"