def predador_de_padroes(digitos):
    # Estratégia: Se 6 ou mais dos últimos 10 dígitos forem < 4, há padrão favorável
    menores_que_4 = [d for d in digitos if d < 4]
    return len(menores_que_4) >= 6