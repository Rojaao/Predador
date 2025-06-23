def predador_de_padroes(digitos):
    menores_que_4 = [d for d in digitos if d < 4]
    return len(menores_que_4) >= 6

def identificador_de_padrao(coletas):
    total = sum(len([d for d in coleta if d < 4]) for coleta in coletas)
    uma_coleta_com_6 = any(len([d for d in coleta if d < 4]) >= 6 for coleta in coletas)
    return total > 15 and uma_coleta_com_6