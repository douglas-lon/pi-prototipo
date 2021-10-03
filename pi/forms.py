from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import (DataRequired, 
                                Email, ValidationError, 
                                EqualTo, Length,
                                )
from flask_login import current_user
from pi.models import Materia, Professor, Aluno
from pi.utils import choices


# Cria o formulário html, utilizando alguns validadores
# nomes dos validadores e dos campos estão em inglês mas são
# autoexplicativos
class RegistroProfessorForm(FlaskForm):
    nome = StringField('Nome', 
                        validators=[DataRequired()],
                        render_kw={"placeholder": "Exemplo: João"}
                        )
    sobrenome = StringField('Sobrenome', 
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Exemplo: Sousa Santos"})
    # cpf = StringField('CPF', validators=[DataRequired(), Length(min=9, max=14)])
    materia = SelectField('Matéria', 
                           choices=choices)
    email = StringField('E-mail', 
                         validators=[DataRequired(), Email()],
                         render_kw={"placeholder": "Exemplo: joão@provedor.com"})
    senha = PasswordField('Senha', 
                           validators=[DataRequired(),
                                       Length(min=8, max=30)],
                           render_kw={"placeholder": "Minímo 8 digitos"})
    confirma_senha = PasswordField('Confirme a Senha', 
                                    validators=[DataRequired(), 
                                                EqualTo('senha'),
                                                Length(min=8, max=30)])
    enviar = SubmitField('Cadastrar')


    # Valida a senha e impede que uma senha tenha
    # espaços como informação
    def validate_senha(self, senha):
        senha_limpa = senha.data.strip()
        if len(senha_limpa) < 8:
            raise ValidationError('Obs: Não adicione espaços na senha')
    
    # Verifica se o email ja está cadastrado, porque ao tentar cadastrar
    # um email já cadastrado da um erro
    def validate_email(self, email):
        email = Professor.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError('Este e-mail já está cadastrado! Por favor escolha outro.')


class LoginProfessorForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', 
                           validators=[DataRequired(),
                                Length(min=8, max=30) 
                                ])
    enviar = SubmitField('Login')


class RegistroMateriaForm(FlaskForm):
    nome = StringField('Nome da Matéria', 
                        validators=[DataRequired(),
                        Length(min=2)],
                        render_kw={"placeholder": "Exemplo: Português"})
    enviar = SubmitField('Adicionar Matéria')

    # Verifica se a materia ja está cadastrado, porque ao tentar cadastrar
    # um materia que já está cadastrado da um erro
    def validate_nome(self, nome):
        materia = Materia.query.filter_by(nome=nome.data).first()
        if materia:
            raise ValidationError('Essa Matéria ja foi adicionada.')


class EditarMateriaForm(FlaskForm):
    nome = StringField('Nome da Matéria', 
                        validators=[DataRequired(),
                        Length(min=2)])
    trocar = SubmitField('Trocar nome da Matéria')



class AtualizarProfessorForm(FlaskForm):
    nome = StringField('Nome', 
                        validators=[DataRequired()],
                        render_kw={"placeholder": "Exemplo: João"}
                        )
    sobrenome = StringField('Sobrenome', 
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Exemplo: Sousa Santos"})
    # cpf = StringField('CPF', validators=[DataRequired(), Length(min=9, max=14)])
    materia = SelectField('Matéria', 
                           choices=choices)
    email = StringField('E-mail', 
                         validators=[DataRequired(), Email()],
                         render_kw={"placeholder": "Exemplo: joão@provedor.com"})
    atualizar = SubmitField('Atualizar')

    # Verifica se o email ja está cadastrado, porque ao tentar cadastrar
    # um email já cadastrado da um erro
    id_prof = ''

    def validate_email(self, email):

        professor = Professor.query.filter_by(email=email.data).first()
        if professor.id != self.id_prof:
                raise ValidationError('Este e-mail já está cadastrado. Por favor escolha outro.')


class TrocarSenhaProfessorForm(FlaskForm):
    senha = PasswordField('Nova Senha', 
                           validators=[DataRequired(),
                                       Length(min=8, max=30)],
                           render_kw={"placeholder": "Minímo 8 digitos"})
    confirma_senha = PasswordField('Confirme a Nova Senha', 
                                    validators=[DataRequired(), 
                                                EqualTo('senha'),
                                                Length(min=8, max=30)])
    trocar = SubmitField('Trocar')


class ConsultarAlunoForm(FlaskForm):
    ra = IntegerField('Ra do Aluno', 
                       validators=[DataRequired()],
                       render_kw={"placeholder": "Exemplo: 78956423"})
    ano = IntegerField('Ano')

    consultar = SubmitField('Consultar')


class AdicionarNotaForm(FlaskForm):
    ra = IntegerField('Ra do Aluno', 
                       validators=[DataRequired()],
                       render_kw={"placeholder": "Exemplo: 78956423"})
    id_materia = IntegerField('Id da Matéria', 
                       validators=[DataRequired()],
                       render_kw={"placeholder": "Exemplo: 2; 'Acessível no Gerenciar Matéria'"})
    nota = StringField('Nota', 
                        validators=[DataRequired()],
                        render_kw={"placeholder": "Exemplo: 8.55"}
                        )
    bimestre = SelectField('Bimestre',
                            choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4')])
    ano = IntegerField('Ano',
                       validators=[DataRequired()])

    adicionar = SubmitField('Adicionar')


class AdicionarAlunoForm(FlaskForm):
    ra = IntegerField('Ra', 
                       validators=[DataRequired()],
                       render_kw={"placeholder": "Exemplo: 78956423"})
    nome = StringField('Nome', 
                        validators=[DataRequired()],
                        render_kw={"placeholder": "Exemplo: Rennan"}
                        )
    sobrenome = StringField('Sobrenome', 
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Exemplo: Guilherme Duarte"})
    turma = StringField('Turma', 
                            validators=[DataRequired()],
                            render_kw={"placeholder": "Exemplo:2 ou 2-A"})

    
    adicionar = SubmitField('Adicionar')

    def validate_ra(self, ra):
        aluno = Aluno.query.filter_by(ra=ra.data).first()

        if aluno:
            raise ValidationError('Um aluno com este RA já existe !')
