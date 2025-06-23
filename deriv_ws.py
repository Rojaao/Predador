import websocket, json, threading
from estrategias import predador_de_padroes, identificador_de_padrao

def iniciar_conexao(token, estrategia, stake, martingale, fator_martingale, placeholder_log):
    def on_open(ws):
        auth = { "authorize": token }
        ws.send(json.dumps(auth))
        placeholder_log.markdown("```text\n✅ Conexão estabelecida com a Deriv!\n```")

    def on_message(ws, message):
        data = json.loads(message)
        if 'msg_type' in data and data['msg_type'] == 'authorize':
            ws.send(json.dumps({
                "ticks_history": "R_100",
                "adjust_start_time": 1,
                "count": 100,
                "end": "latest",
                "start": 1,
                "style": "ticks",
                "subscribe": 1
            }))
        if 'msg_type' in data and data['msg_type'] == 'history':
            ultimos_digitos = [int(str(tick)[-1]) for tick in data['history']['prices'][-10:]]
            if estrategia == "Predador de Padrões":
                predador_de_padroes(ultimos_digitos, ws, stake, martingale, fator_martingale, placeholder_log)
            elif estrategia == "Identificador de Padrão":
                identificador_de_padrao(ultimos_digitos, ws, stake, martingale, fator_martingale, placeholder_log)

    def on_error(ws, error):
        placeholder_log.markdown(f"```text\n❌ Erro: {error}\n```")

    def on_close(ws, *args):
        placeholder_log.markdown("```text\n🔌 Conexão encerrada.\n```")

    def run():
        ws = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id=1089",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
        ws.run_forever()

    threading.Thread(target=run).start()