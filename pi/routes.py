from flask import render_template, url_for
from pi import app


@app.route("/")
@app.route("/home/")
def home():
    titulo = 'Inicio'
    return render_template('home.html', titulo=titulo)

@app.route("/aluno/")
def aluno():
    titulo = "Aluno"
    return render_template('aluno.html', titulo=titulo, user='aluno')


@app.route("/professor/")
def professor():
    titulo = "Professor"
    return render_template('professor.html', titulo=titulo, user='professor')

