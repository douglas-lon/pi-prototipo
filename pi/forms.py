from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, 
                                Email, ValidationError, EqualTo)

class RegistroProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', DataRequired(), Email())
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirma_senha = PasswordField('Confime a Senha', validators=[DataRequired(), EqualTo('senha')])
    enviar = SubmitField('Registrar-Se')

class LoginProfessorForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    enviar = SubmitField('Login')
