import websocket, json, threading, time
from estrategias import predador_de_padroes, identificador_padrao

def iniciar_conexao(token, stake, martingale, estrategia, atualizar_interface):
    msg_log = []
    def log(msg):
        msg_log.append(msg)
        if len(msg_log) > 50:
            msg_log.pop(0)
        atualizar_interface("\n".join(msg_log))

    def on_open(ws):
        log("✅ Conectado à Deriv!")
        auth_req = { "authorize": token }
        ws.send(json.dumps(auth_req))

    def on_message(ws, message):
        data = json.loads(message)
        if 'error' in data:
            log("❌ Erro: " + str(data['error']['message']))
            return

        if data.get("msg_type") == "authorize":
            log("🔐 Autorizado com sucesso.")
            ws.send(json.dumps({ "ticks_history": "R_100", "adjust_start_time": 1, "count": 10, "end": "latest", "style": "ticks", "granularity": 1 }))
        elif data.get("msg_type") == "history":
            ultimos_digitos = [int(str(d)[-1]) for d in data['history']['prices']]
            log(f"📊 Dígitos recebidos: {ultimos_digitos}")

            if estrategia == "Predador de Padrões":
                decisao = predador_de_padroes(ultimos_digitos)
            else:
                decisao = identificador_padrao(ultimos_digitos)

            if decisao:
                log("🎯 Enviando entrada Over 3...")
                buy_contract = {
                    "buy": 1,
                    "price": stake,
                    "parameters": {
                        "amount": stake,
                        "basis": "stake",
                        "contract_type": "DIGITOVER",
                        "currency": "USD",
                        "duration": 1,
                        "duration_unit": "t",
                        "symbol": "R_100",
                        "barrier": "3"
                    }
                }
                ws.send(json.dumps(buy_contract))
            else:
                log("⏸️ Padrão não favorável. Aguardando...")

    def on_error(ws, error):
        log(f"❌ Erro: {error}")

    def on_close(ws, *args):
        log("🔌 Conexão encerrada.")

    def run():
        ws.run_forever()

    ws = websocket.WebSocketApp("wss://ws.deriv.com/websockets/v3",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    thread = threading.Thread(target=run)
    thread.start()
