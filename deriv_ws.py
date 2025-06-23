
import websocket
import threading
import json

def iniciar_conexao(token, atualizar_interface):
    def on_open(ws):
        atualizar_interface("✅ Conexão estabelecida com a Deriv!")
        ws.send(json.dumps({
            "ticks": "R_100",
            "subscribe": 1
        }))

    def on_message(ws, message):
        atualizar_interface(f"📩 Mensagem recebida: {message}")

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws, *args):
        atualizar_interface("🔌 Conexão encerrada.")

    url = "wss://ws.binaryws.com/websockets/v3?app_id=1089&l=EN&brand=deriv"
    ws_app = websocket.WebSocketApp(
        url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        header={"Authorization": f"Bearer {token}"}
    )

    threading.Thread(target=ws_app.run_forever).start()
