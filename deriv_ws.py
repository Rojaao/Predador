import websocket, json, threading, time
from estrategias import predador_de_padroes, identificador_padrao

def iniciar_conexao(token, stake, martingale, estrategia, atualizar_interface):
    def on_open(ws):
        ws.send(json.dumps({"authorize": token}))
        atualizar_interface("✅ Conexão estabelecida com a Deriv!")
        ws.send(json.dumps({"ticks_history": "R_100", "count": 100, "end": "latest", "style": "ticks", "granularity": 1, "subscribe": 1, "req_id": "1"}))

    def on_message(ws, message):
        msg = json.loads(message)
        if "history" in msg:
            ultimos = list(map(int, msg["history"]["prices"][-10:]))
            if estrategia == "Predador de Padrões":
                predador_de_padroes(ws, ultimos, stake, martingale)
            elif estrategia == "Identificador de Padrão":
                identificador_padrao(ws, ultimos, stake, martingale)

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws, *args):
        atualizar_interface("🔌 Conexão encerrada.")

    def run():
        ws_app = websocket.WebSocketApp(
            "wss://ws.derivws.com/websockets/v3?app_id=1089",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws_app.run_forever()

    threading.Thread(target=run).start()