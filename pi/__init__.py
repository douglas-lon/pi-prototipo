from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager

# Instancia principal da classe flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Não tão secreta por agora'
# Adiciona a localização do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pi.db'

# Inicia a instancia do SQLAlchemy que server para fazer conexões
# no banco de dados utilizando o flask
db = SQLAlchemy(app)
# Instancia do Bcrypt que serve para criptografar e verificar 
bcrypt = Bcrypt(app)
# Instancia do login manager, server para logar um usuário 
# e impedir que usuários não logados tenham acesso a certos lugares
login_manager = LoginManager(app)
# especifica o app.route que é da página de login
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Customiza a mensagem gerada ao tentar entrar em uma pagina restrita sem
# estar logado
login_manager.login_message = "Por favor faça login para acessar essa página"

# Necessário importar os routes aqui embaixo para não dar conflito
from pi import routes