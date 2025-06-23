def predador_de_padroes(digitos):
    abaixo_de_4 = [d for d in digitos if d < 4]
    return len(abaixo_de_4) >= 6

def identificador_padrao(digitos):
    # Placeholder simples para segunda estratégia
    pares = [d for d in digitos if d % 2 == 0]
    return len(pares) >= 5
