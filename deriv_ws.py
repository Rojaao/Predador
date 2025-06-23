import websocket
import json
import threading

def iniciar_conexao(token, stake, estrategia_func, atualizar_interface):
    def on_open(ws):
        atualizar_interface("✅ Conexão estabelecida com a Deriv!")
        auth_data = {
            "authorize": token
        }
        ws.send(json.dumps(auth_data))

    def on_message(ws, message):
        data = json.loads(message)
        if 'msg_type' in data:
            if data['msg_type'] == 'authorize':
                atualizar_interface("🔐 Autorizado com sucesso!")
                estrategia_func(ws, stake, atualizar_interface)
            elif data['msg_type'] == 'error':
                atualizar_interface(f"❌ Erro da API: {data['error']['message']}")

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

    thread = threading.Thread(target=run)
    thread.start()