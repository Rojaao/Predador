
import random

def predador_de_padroes(digitos):
    abaixo_de_4 = [d for d in digitos if d < 4]
    if len(abaixo_de_4) >= 6:
        return "OVER"
    return None

def identificador_de_padrao(coletas):
    total_digitos = sum(len(c) for c in coletas)
    total_abaixo_de_4 = sum(d < 4 for coleta in coletas for d in coleta)
    passou_50 = total_abaixo_de_4 / total_digitos > 0.5
    algum_6oumais = any(sum(d < 4 for d in coleta) >= 6 for coleta in coletas)
    if passou_50 and algum_6oumais:
        return "OVER"
    return None
