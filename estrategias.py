def predador_de_padroes(ticks, ws, token):
    abaixo_de_4 = [tick for tick in ticks[-8:] if tick % 10 < 4]
    if len(abaixo_de_4) >= 6:
        contrato = {
            "buy": 1,
            "price": 1,
            "parameters": {
                "amount": 1,
                "basis": "stake",
                "contract_type": "CALL",
                "currency": "USD",
                "duration": 1,
                "duration_unit": "t",
                "symbol": "R_100"
            },
            "subscribe": 1
        }
        ws.send(json.dumps(contrato))

def identificador_de_padrao(ticks, ws, token):
    # Estratégia de exemplo simplificada para este envio
    contrato = {
        "buy": 1,
        "price": 1,
        "parameters": {
            "amount": 1,
            "basis": "stake",
            "contract_type": "CALL",
            "currency": "USD",
            "duration": 1,
            "duration_unit": "t",
            "symbol": "R_100"
        },
        "subscribe": 1
    }
    ws.send(json.dumps(contrato))
