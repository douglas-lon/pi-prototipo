from flask import render_template, url_for, abort, redirect, flash, request
from pi import app, db, bcrypt, login_manager
from pi.forms import LoginProfessorForm, RegistroProfessorForm, RegistroMateriaForm
from pi.models import Professor, Materia
from flask_login import login_user, current_user, logout_user, login_required
from pi.utils import choices, atualiza_escolhas



@app.route("/")
@app.route("/home/")
def home():
    # Carrega página inicial especificada abaixo
    titulo = 'Inicio'
    return render_template('home.html', titulo=titulo)

@app.route("/aluno/")
def aluno():
    #Carrega do aluno especificada abaixo
    titulo = "Aluno"
    return render_template('aluno.html', 
                           titulo=titulo, user='aluno')


@app.route("/aluno/consulta/<info>/")
def aluno_consulta(info):
    # Pega a informação digitada a frente consulta/ 
    # e carrega a pagina especificada abaixo passando essa informação
    # como parametro para modificar a página baseada neça
    if info in ['situacao', 'informacao']:
        return render_template('consulta.html', 
                               info=info, user='aluno')
    else:
        # Se a informação passada não for uma das acima
        # ele joga um erro de página não encontrada
        abort(404)
    

@app.route("/professor/")
@login_required
def professor():
    # Necesário estar logado para acesso
    # Página princinpal do professor onde daqui ele pode acessar
    # outras funcionalidades e informações e por isso login é necessário
    # para impedir outras pessoas de mexer nas informações 
    titulo = "Professor"
    return render_template('professor.html', 
                           titulo=titulo, user='professor')


@app.route("/login/", methods=["GET", "POST"])
def login():
    # Página de login 

    if current_user.is_authenticated:
        # Redireciona o usuário para a página do professor se ele tentar
        # fazer login estando ja logado
        return redirect(url_for('professor'))

    # Inicia instancia do Formulário de login
    form = LoginProfessorForm()
    if form.validate_on_submit():
        # Se o formulário passar as validações especificadas
        # no forms.py para ele, tentará fazer login
        # com as informações especificadas e se as informações
        # estiverem erradas ou não existirem ele retorna uma mensagem

        professor = Professor.query.filter_by(
                        email=form.email.data).first()

        if professor and bcrypt.check_password_hash(
                            professor.senha, 
                            form.senha.data):
            # descriptografa a senha e 
            # Se as  informações estiverem certas
            # Ele fara login e será redirecionado para a
            # página do professor
            # Se o usuário tentar entrar em uma página que necessita de login
            # ele virá para a página de login e se ele fizer login ele voltará
            # para a página que ele estava tentando acessar

            login_user(professor)
            pagina_alvo = request.args.get('next')
            if pagina_alvo:
                return redirect(pagina_alvo)
            else:
                return redirect(url_for('professor'))
        else:
            flash('Falha no login. Por favor cheque email e senha.', 'danger')

    return render_template('login.html', 
                            titulo='Login', form=form, user="login")


@app.route("/registrar/", methods=["GET", "POST"])
@login_required
def registrar():
    # Se o formulário passar as validações especificadas
    # no forms.py para ele, irá registrar o professor

    form = RegistroProfessorForm()
    if form.validate_on_submit():
        # criptografa senha para não salva-la em texto
        senha_cript = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')

        # Adiciona as informações na tabela
        professor = Professor(nome=form.nome.data.strip(),
                              sobrenome=form.sobrenome.data.strip(),
                              materia=form.materia.data,
                              email=form.email.data,
                              senha=senha_cript,
                              )

        # Envia elas para o banco de dados
        # e redireciona para a pagina do professor
        db.session.add(professor)
        db.session.commit()
        flash(f'Conta criada para {form.nome.data}!', 'success')
        return redirect(url_for('professor'))

    return render_template('registrar.html', 
                            titulo='Registrar', 
                            form=form, user="registro")


@app.route("/registrar/materia/", methods=["GET", "POST"])
@login_required
def registrar_materia():
    # Se o formulário passar as validações especificadas
    # no forms.py para ele, irá registrar uma matéria
    form = RegistroMateriaForm()
    if form.validate_on_submit():
        # Adiciona as informações na tabela
        materia = Materia(nome=form.nome.data.strip())

        # Envia elas para o banco de dados
        # e redireciona para a pagina do professor
        db.session.add(materia)
        db.session.commit()
        flash(f'A matéria {form.nome.data} foi adicionada!', 'success')

        atualiza_escolhas(choices)

        return redirect(url_for('professor'))

    return render_template('registrar.html', 
                           titulo='Registrar Materia', 
                           form=form, user="materia")

@app.route("/gerenciar/materia/", methods=["GET", "POST"])
@login_required
def gerenciar_materia():
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        t = request.form['text']
        try:
            t = int(t)
        except:
            flash('Digite um número de id!', 'info')
            return redirect(url_for('gerenciar_materia'))
        print('===========')
        print(t)
        print('===========')
        return redirect(url_for('apagar_materia', id_materia=t))

    materias = Materia.query.paginate(per_page=8)
    return render_template('gerenciar.html', 
                            titulo='Gerenciar Materia', 
                            user='materia',
                            lista_materias=materias)

@app.route("/gerenciar/materia/apagar/<id_materia>", methods=['GET', 'POST'])
@login_required
def apagar_materia(id_materia):
    materia = Materia.query.get_or_404(id_materia)
    try:
        materia_nome = materia.nome
    except:
        flash('Você tentou apagar um matéria que não existe', 'danger')
        return redirect(url_for('gerenciar_materia'))
    db.session.delete(materia)
    db.session.commit()
    flash(f'A matéria {materia_nome} foi deletada!', 'success')
    return redirect(url_for('gerenciar_materia'))

@app.route("/logout/")
def logout():
    # Sai do usuário logado
    logout_user()
    return redirect(url_for('home'))