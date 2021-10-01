from flask import render_template, url_for, abort, redirect, flash
from pi import app
from pi.forms import LoginProfessorForm, RegistroProfessorForm
from pi.models import Professor


@app.route("/")
@app.route("/home/")
def home():
    titulo = 'Inicio'
    return render_template('home.html', titulo=titulo)

@app.route("/aluno/")
def aluno():
    titulo = "Aluno"
    return render_template('aluno.html', 
                           titulo=titulo, user='aluno')


@app.route("/aluno/consulta/<info>/")
def aluno_consulta(info):
    if info in ['situacao', 'informacao']:
        return render_template('consulta.html', 
                               info=info, user='aluno')
    else:
        abort(404)
    

@app.route("/professor/")
def professor():
    titulo = "Professor"
    return render_template('professor.html', 
                           titulo=titulo, user='professor')


@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginProfessorForm()
    if form.validate_on_submit():
        professor = Professor.query.filter_by(email=form.email.data).first()
        
        if professor:
            return redirect(url_for('professor'))
        else:
            flash('Falha no login. Por favor cheque email e senha.', 'danger')

    return render_template('login.html', titulo='Login', form=form, user="login")


@app.route("/registrar/", methods=["GET", "POST"])
def registrar():
    form = RegistroProfessorForm()
    if form.validate_on_submit():
        flash(f'Conta cria para {form.nome.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('registrar.html', titulo='Registrar', form=form, user="registro")