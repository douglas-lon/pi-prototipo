from pi.models import Materia, NotaAluno

choices = []

def atualiza_escolhas(choices):
    choices.clear()
    for choice in Materia.query.all():
        choices.append((choice.id, choice.nome))


def calcular_desempenho(id_aluno, bimestre, ano):

    # baixo = < 4
    # 4 < insatisfatorio < 5 três notas
    # 4 < satisfatorio < 5 duas notas
    # 5 < Muito bom 
    checagem = {
        'baixo': 0,
        'insatisfatorio': 0,
        'bom': 0,
    }


    notas = NotaAluno.query.filter_by(id_aluno=id_aluno, bimestre=bimestre, ano=ano).all()
    qtd_nota = len(notas)

    for nota in notas:
        if 0 < float(nota.nota) < 4:
            checagem['baixo'] += 1
        elif 4 < float(nota.nota) < 5:
            checagem['insatisfatorio'] += 1
        
        if float(nota.nota) >= 5:
            checagem['bom'] += 1
    
    resultado = ''
    cor = ''
    if checagem['baixo'] == 0 and checagem['insatisfatorio'] == 0  and checagem['bom'] == 0:
        resultado = 'Ainda sem notas'
        cor = 'sem-notas'
    elif checagem['baixo'] > 3:
        resultado =  'Baixo Rendimento'
        cor = 'baixo-rendimento'
    elif  2 < checagem['insatisfatorio'] <= 3:
        resultado =  'Resultado insatisfatório'
        cor = 'resultado-insatisfatorio'
    elif  checagem['insatisfatorio'] <= 2:
        resultado =  'Resultado satisfatório'
        cor = 'resultado-satisfatorio'
    elif checagem['bom'] == qtd_nota:
        resultado = 'Resultado acima da média'
        cor = 'resultado-acima-da-media'

    return resultado, cor, checagem
    
atualiza_escolhas(choices)
