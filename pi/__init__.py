from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Não tão secreta por agora'


from pi import routes