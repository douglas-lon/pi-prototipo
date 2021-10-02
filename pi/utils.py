from pi.models import Materia

choices = []

def atualiza_escolhas(choices):
    choices.clear()
    for choice in Materia.query.all():
        choices.append((choice.id, choice.nome))


atualiza_escolhas(choices)
