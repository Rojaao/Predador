def predador_de_padroes(digitos, ws, stake, martingale, fator, log):
    qtd = sum(1 for d in digitos if d < 4)
    log.markdown(f"```text\n📊 Últimos dígitos: {digitos}\nDígitos <4: {qtd}/10\n```")
    if qtd >= 6:
        ws.send(json.dumps({
            "buy": 1,
            "price": stake,
            "parameters": {
                "contract_type": "CALL",
                "symbol": "R_100",
                "duration": 1,
                "duration_unit": "t",
                "barrier": "3",
                "basis": "stake"
            }
        }))

def identificador_de_padrao(digitos, ws, stake, martingale, fator, log):
    qtd = sum(1 for d in digitos if d < 4)
    log.markdown(f"```text\n🧠 Análise Identificador: {digitos} <4: {qtd}\n```")
    if qtd >= 5:
        ws.send(json.dumps({
            "buy": 1,
            "price": stake,
            "parameters": {
                "contract_type": "CALL",
                "symbol": "R_100",
                "duration": 1,
                "duration_unit": "t",
                "barrier": "3",
                "basis": "stake"
            }
        }))