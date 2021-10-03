from datetime import date
from enum import unique
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


class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ra = db.Column(db.Integer, unique=True, nullable=False)
    nome = db.Column(db.String(20), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    turma = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Aluno('{self.id}', '{self.ra}', '{self.nome}')"


class NotaAluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey('materia.id'), nullable=False)
    nota = db.Column(db.String(5), nullable=False)
    bimestre = db.Column(db.Integer, nullable=False)
    ano = db.Column(db.SmallInteger, nullable=False, default=date.today().year)

    def __repr__(self):
        return f"Nota('{self.id}', '{self.id_aluno}', '{self.id_materia}', '{self.nota}', '{self.bimestre}', '{self.ano}')"
