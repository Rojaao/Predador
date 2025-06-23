
import random

def predador_de_padroes(digitos):
    abaixo_de_4 = [d for d in digitos if d < 4]
    return len(abaixo_de_4) >= 6

def identificador_de_padrao(coletas):
    if len(coletas) < 3:
        return False

    total_digitos = sum(len(c) for c in coletas)
    total_abaixo_4 = sum(1 for c in coletas for d in c if d < 4)
    uma_coleta_com_6 = any(sum(1 for d in c if d < 4) >= 6 for c in coletas)

    return (total_abaixo_4 / total_digitos) > 0.5 and uma_coleta_com_6
