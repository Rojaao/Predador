
import websocket
import json
import threading

def iniciar_conexao(token, atualizar_interface, estrategia):
    def on_open(ws):
        ws.send(json.dumps({"authorize": token}))
        atualizar_interface("✅ Conexão estabelecida com a Deriv!")

    def on_message(ws, message):
        data = json.loads(message)
        atualizar_interface(f"📩 Mensagem recebida: {data}")

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws, *args):
        atualizar_interface("🔌 Conexão encerrada.")

    def run():
        ws_app = websocket.WebSocketApp(
            "wss://ws.derivws.com/websockets/v3",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws_app.run_forever()

    threading.Thread(target=run).start()
