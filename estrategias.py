import time

def predador_de_padroes(digitos):
    """Se 6 ou mais dos últimos 10 dígitos forem < 4."""
    menores_que_4 = [d for d in digitos if d < 4]
    return len(menores_que_4) >= 6

def identificador_de_padrao(send_request_func, atualizar_log, delay1=3, delay2=5):
    """Executa 3 coletas de 10 dígitos usando send_request_func.
    send_request_func deve enviar um request de ticks_history e retornar lista de dígitos.
    atualizar_log registra status. """
    # 1ª coleta
    atualizar_log('🔍 Identificador: 1ª coleta de 10 dígitos...')
    digitos1 = send_request_func()
    atualizar_log(f'📊 Coleta1: {digitos1}')
    time.sleep(delay1)
    # 2ª coleta
    atualizar_log('🔍 Identificador: 2ª coleta de 10 dígitos...')
    digitos2 = send_request_func()
    atualizar_log(f'📊 Coleta2: {digitos2}')
    time.sleep(delay2)
    # 3ª coleta
    atualizar_log('🔍 Identificador: 3ª coleta de 10 dígitos...')
    digitos3 = send_request_func()
    atualizar_log(f'📊 Coleta3: {digitos3}')
    # Combina
    todos = digitos1 + digitos2 + digitos3
    cnt_menor4 = sum(1 for d in todos if d < 4)
    cond1 = cnt_menor4 > 15  # >50% de 30
    cond2 = (sum(1 for d in digitos1 if d < 4) >= 6 or 
             sum(1 for d in digitos2 if d < 4) >= 6 or 
             sum(1 for d in digitos3 if d < 4) >= 6)
    atualizar_log(f'🔎 Identificador: total <4: {cnt_menor4}/30, cond1:%>{cnt_menor4>15}, cond2:{cond2}')
    return cond1 and cond2