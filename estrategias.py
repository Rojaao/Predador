def predador_de_padroes(ws, ultimos, stake, martingale):
    qtd = sum(1 for d in ultimos if d < 4)
    if qtd >= 6:
        ws.send('{"buy": 1, "price": ' + str(stake) + ', "parameters": {"contract_type": "CALL", "symbol": "R_100", "duration": 1, "duration_unit": "t", "barrier": "3"}, "subscribe": 1}')

def identificador_padrao(ws, ultimos, stake, martingale):
    # Apenas exemplo básico da lógica futura
    qtd = sum(1 for d in ultimos if d < 4)
    if qtd >= 6:
        ws.send('{"buy": 1, "price": ' + str(stake) + ', "parameters": {"contract_type": "CALL", "symbol": "R_100", "duration": 1, "duration_unit": "t", "barrier": "3"}, "subscribe": 1}')