from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import (DataRequired, 
                                Email, ValidationError, 
                                EqualTo, Length,
                                )
from pi.models import Materia, Professor
from pi.utils import choices


# Cria o formulário html, utilizando alguns validadores
# nomes dos validadores e dos campos estão em inglês mas são
# autoexplicativos
class RegistroProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    # cpf = StringField('CPF', validators=[DataRequired(), Length(min=9, max=14)])
    materia = SelectField('Matéria', 
                           choices=choices)
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', 
                           validators=[DataRequired(),
                                       Length(min=8, max=30)
                                       ])
    confirma_senha = PasswordField('Confirme a Senha', 
                                    validators=[DataRequired(), 
                                                EqualTo('senha'),
                                                Length(min=8, max=30)
                                                ])
    enviar = SubmitField('Registrar-Se')


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
            raise ValidationError('Este e-mail já está cadastrado!')


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
                        Length(min=2)
                        ])
    enviar = SubmitField('Registrar Matéria')

    # Verifica se a materia ja está cadastrado, porque ao tentar cadastrar
    # um materia que já está cadastrado da um erro
    def validate_nome(self, nome):
        materia = Materia.query.filter_by(nome=nome.data).first()
        if materia:
            raise ValidationError('Essa Matéria ja foi adicionada.')