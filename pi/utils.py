from pi.models import Materia

choices = []

def atualiza_escolhas(choices):
    for choice in Materia.query.all():
        choices.append((choice.id, choice.nome))

atualiza_escolhas(choices)