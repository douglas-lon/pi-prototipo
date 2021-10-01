from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import (DataRequired, 
                                Email, ValidationError, 
                                EqualTo, Length,
                                )

class RegistroProfessorForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    # cpf = StringField('CPF', validators=[DataRequired(), Length(min=9, max=14)])
    materia = SelectField('Matéria', 
                           choices=[
                                ('Nenhuma', 'Nenhuma'),
                                ('Matemática', 'Matemática'),
                                ('Português', 'Português')
                                ])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', 
                           validators=[DataRequired(),
                                       Length(min=8, max=30)
                                       ])
    confirma_senha = PasswordField('Confime a Senha', 
                                    validators=[DataRequired(), 
                                                EqualTo('senha'),
                                                Length(min=8, max=30)
                                                ])
    enviar = SubmitField('Registrar-Se')

class LoginProfessorForm(FlaskForm):
    email = StringField('E-mail',
                        validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', 
                           validators=[DataRequired(),
                                Length(min=8, max=30) 
                                ])
    enviar = SubmitField('Login')
