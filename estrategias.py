def predador_de_padroes(digitos):
    """
    Estratégia 'Predador de Padrões':
    Se 6 ou mais dos últimos 10 dígitos forem menores que 4, o padrão é considerado favorável.
    """
    menores_que_4 = [d for d in digitos if d < 4]
    return len(menores_que_4) >= 6
