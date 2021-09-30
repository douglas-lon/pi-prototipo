from flask import render_template, url_for, abort
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


@app.route("/aluno/consulta/<info>/")
def aluno_consulta(info):
    if info in ['situacao', 'informacao']:
        return render_template('consulta.html', info=info, user='aluno')
    else:
        abort(404)
    

@app.route("/professor/")
def professor():
    titulo = "Professor"
    return render_template('professor.html', titulo=titulo, user='professor')

