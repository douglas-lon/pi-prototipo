from flask import render_template, url_for, abort, redirect, flash, request
from datetime import date
from pi import app, db, bcrypt, login_manager
from pi.forms import (LoginProfessorForm, RegistroProfessorForm, 
                      RegistroMateriaForm,AtualizarProfessorForm, 
                      TrocarSenhaProfessorForm,
                      EditarMateriaForm, AdicionarAlunoForm, ConsultarAlunoForm,
                      AdicionarNotaForm)
from pi.models import NotaAluno, Professor, Materia, Aluno
from flask_login import login_user, current_user, logout_user, login_required
from pi.utils import choices, atualiza_escolhas, calcular_desempenho



@app.route("/")
@app.route("/home/")
def home():
    # Carrega página inicial especificada abaixo
    titulo = 'Inicio'
    return render_template('home.html', titulo=titulo)

# Inicio das funções sobre o Aluno


@app.route("/aluno/")
def aluno():
    #Carrega do aluno especificada abaixo
    titulo = "Aluno"
    return render_template('aluno.html', 
                           titulo=titulo, user='aluno')


@app.route("/registrar/aluno/", methods=["GET", "POST"])
def registrar_aluno():

    form = AdicionarAlunoForm()

    if form.validate_on_submit():

            aluno = Aluno(ra=form.ra.data,
                          nome=form.nome.data,
                          sobrenome=form.sobrenome.data,
                          turma=form.turma.data)

            db.session.add(aluno)
            db.session.commit()
            flash(f'Aluno {form.nome.data} foi adicionado!', 'success')
            return redirect(url_for('professor'))

    return render_template('registrar_aluno.html', 
                            titulo='Adicionar Aluno', 
                            form=form, user="registro")


@app.route("/professor/consulta/", methods=["GET", "POST"])
def consultar_aluno():

    form = ConsultarAlunoForm()

    if form.validate_on_submit():
        aluno = Aluno.query.filter_by(ra=form.ra.data).first()
        if aluno:
            return redirect(url_for('consultar_aluno_ra', 
                                    ra_aluno=form.ra.data,
                                    ano=form.ano.data,
                                    bimestre=1))
        else:
            flash('Aluno com este RA não foi encontrado!', 'info')

    form.ano.data = date.today().year
        
    
    return render_template('consulta.html', 
                            titulo='Consultar Aluno',
                            form=form,
                            user="professor")

@app.route("/aluno/consultar/", methods=["GET", "POST"])
def aluno_consulta():
    form = ConsultarAlunoForm()

    if form.validate_on_submit():
        aluno = Aluno.query.filter_by(ra=form.ra.data).first()
        if aluno:
            return redirect(url_for('consultar_aluno_ra', 
                                    ra_aluno=form.ra.data,
                                    ano=form.ano.data,
                                    bimestre=1))
        else:
            flash('Aluno com este RA não foi encontrado!', 'info')

    form.ano.data = date.today().year
    
    return render_template('aluno_consulta.html', 
                            titulo='Consultar Aluno',
                            form=form,
                            user="aluno")

@app.route("/consultar/aluno/")
def consultar_aluno_ra():
    ano = request.args.get('ano', int)
    ra_aluno = request.args.get('ra_aluno', int)
    
    bimestre = request.args.get('bimestre', int)

    aluno = Aluno.query.filter_by(ra=ra_aluno).first()

    desempenho, cor, c = calcular_desempenho(aluno.id, bimestre, ano)
    print('=============')
    print(c)

    return render_template('consulta_aluno.html', 
                            titulo='Consultar Aluno',
                            aluno=aluno,
                            ano=ano,
                            bimestre=bimestre,
                            desempenho=desempenho,
                            cor=cor,
                            nota_aluno=NotaAluno,
                            materia=Materia,
                            user="professor")

@app.route("/consultar/professor/", methods=["GET", "POST"])
def consultar_professor():
    form = ConsultarAlunoForm()

    if form.validate_on_submit():
        aluno = Aluno.query.filter_by(ra=form.ra.data).first()
        if aluno:
            return redirect(url_for('consultar_aluno_ra', 
                                    ra_aluno=form.ra.data,
                                    ano=form.ano.data,
                                    bimestre=1))
        else:
            flash('Aluno com este RA não foi encontrado!', 'info')

    form.ano.data = date.today().year
    
    return render_template('aluno_consulta.html', 
                            titulo='Consultar Aluno',
                            form=form,
                            user="aluno")


@app.route("/professor/registrar/nota/", methods=["GET", "POST"])
def adicionar_nota():

    form = AdicionarNotaForm()
    if form.validate_on_submit():
        aluno = Aluno.query.filter_by(ra=form.ra.data).first()
        id_aluno = ''
        try:
            id_aluno = aluno.id
        except:
            flash('Nenhum aluno com este RA encontrado', 'info')
            return redirect(url_for('adicionar_nota'))

        
        nota = NotaAluno(id_aluno=id_aluno, 
                         id_materia=form.id_materia.data,
                         nota=form.nota.data,
                         bimestre=form.bimestre.data,
                         ano=form.ano.data)
        
        db.session.add(nota)
        db.session.commit()

        flash(f'Nota de {form.nota.data} foi adicionado para o aluno {aluno.nome}!', 'success')
        return redirect(url_for('professor'))

    elif request.method == "GET":
        form.ano.data = date.today().year

    return render_template('adicionar_nota.html', 
                            titulo='Adicionar Nota',
                            form=form,
                            user="professor")

# Fim das funções sobre o Aluno


# Inicio das funções sobre o professor


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


@app.route("/logout/")
def logout():
    # Sai do usuário logado
    logout_user()
    return redirect(url_for('home'))


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


@app.route("/gerenciar/professor/")
def gerenciar_professor():
    page = request.args.get('page', 1, type=int)
    professores = Professor.query.paginate(per_page=6)

    return render_template('gerenciar_professores.html', 
                            titulo='Gerenciar Professores', 
                            user="gerenciar",
                            lista_professores=professores,
                            materia=Materia)


@app.route("/gerenciar/editar/<id_professor>/", methods=["GET", "POST"])
def editar_professor(id_professor):
    professor = Professor.query.get_or_404(id_professor)
    
    form = AtualizarProfessorForm()
    form.id_prof = professor.id
    
    if form.validate_on_submit():
        professor.nome = form.nome.data
        professor.sobrenome = form.sobrenome.data
        professor.email = form.email.data
        professor.materia = form.materia.data
        db.session.commit()

        flash(f'O professor {form.nome.data} foi atualizado!', 'success')
        return redirect(url_for('gerenciar_professor'))

    elif request.method == 'GET':
        materia_nome = Materia.query.filter_by(id=professor.materia).first()
        try:
            materia_nome = materia_nome.nome
        except:
            flash('Professor sem matéria!', 'info')

        
        escolhas_especificas = choices.copy()
        if materia_nome:
            escolhas_especificas.remove((professor.materia, materia_nome))
            escolhas_especificas.insert(0, (professor.materia, materia_nome))


        form.nome.data = professor.nome
        form.sobrenome.data = professor.sobrenome
        form.email.data = professor.email
        form.materia.choices = escolhas_especificas
    

    return render_template('editar_professor.html', 
                            titulo='Editar Professor', 
                            user="editar",
                            id_professor = professor.id,
                            form=form)

@app.route("/gerenciar/editar/senha/<id_professor>/", methods=["GET", "POST"])
def trocar_senha(id_professor):
    professor = Professor.query.get_or_404(id_professor)
    form = TrocarSenhaProfessorForm()

    if form.validate_on_submit():
        senha_cript = bcrypt.generate_password_hash(form.senha.data).decode('utf-8')
        professor.senha = senha_cript
        db.session.commit()

        flash(f'A senha do professor {professor.nome} foi alterada!', 'success')
        return redirect(url_for('gerenciar_professor'))

    return render_template('trocar.html', 
                            titulo='Trocar Senha', 
                            user="editar",
                            form=form,
                            professor_nome=professor.nome)


# Fim das funções do professor


@app.route("/gerenciar/apagar/<info>/", methods=["GET", "POST"])
def apagar(info):

    info = info
    list_info = info.split(';')

    try:
        list_info[0] = int(list_info[0])
        list_info[2] = eval(list_info[2])
    except:
        flash('Por favor acesse essa página da maneira correta!', 'info')
        return redirect(url_for('professor'))

    if list_info[2]:
        if list_info[1] == 'materia':
            materia = Materia.query.get_or_404(list_info[0])
            materia_nome = materia.nome

            db.session.delete(materia)
            db.session.commit()
            flash(f'A matéria {materia_nome} foi apagada', 'success')
            return redirect(url_for('gerenciar_materia'))

        elif list_info[1] == 'professor':
            professor = Professor.query.get_or_404(list_info[0])
            professor_nome = professor.nome

            db.session.delete(professor)
            db.session.commit()
            
            flash(f'O professor {professor_nome} foi apagado do registro', 'success')
            return redirect(url_for('gerenciar_professor'))
    
    return render_template('apagar.html',
                            titulo='Apagar',
                            info=info,
                            user='apagar')


# Inicio das funções sobre matéria


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

    materias = Materia.query.paginate(per_page=6)
    return render_template('gerenciar_materias.html', 
                            titulo='Gerenciar Materias', 
                            user='gerenciar',
                            lista_materias=materias)


@app.route("/gerenciar/materia/<id_materia>/", methods=["GET", "POST"])
def editar_materia(id_materia):
    id_mat = id_materia

    materia = Materia.query.get_or_404(id_materia)
    materia_nome = materia.nome
    form = EditarMateriaForm()
    if form.validate_on_submit():
        materia.nome = form.nome.data
        db.session.commit()
        flash(f'O nome da matéria {materia_nome} foi alterada para {form.nome.data}!', 'success')

        atualiza_escolhas(choices)

        return redirect(url_for('gerenciar_materia'))

    elif request.method == 'GET':
        form.nome.data = materia.nome


    return render_template('trocar.html', 
                            titulo='Trocar Materia', 
                            user='materia',
                            form=form,
                            id_mat=id_mat)


# Fim das funções sobre matéria