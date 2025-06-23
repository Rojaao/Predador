import websocket
import json

def iniciar_robo(token):
    def on_open(ws):
        print("🟢 Conectado com sucesso. Autenticando...")
        ws.send(json.dumps({"authorize": token}))

    def on_message(ws, message):
        data = json.loads(message)
        print(f"📩 Mensagem: {data}")
        if data.get("msg_type") == "authorize":
            print("✅ Autenticado com sucesso!")
            ws.send(json.dumps({
                "ticks_history": "R_100",
                "adjust_start_time": 1,
                "count": 10,
                "end": "latest",
                "start": 1,
                "style": "ticks"
            }))
        elif data.get("msg_type") == "history":
            print("🎯 Recebido histórico de ticks:", data["history"]["prices"])
            ws.close()

    def on_error(ws, error):
        print(f"❌ Erro: {error}")

    def on_close(ws, *args):
        print("🔌 Conexão encerrada.")

    ws = websocket.WebSocketApp(
        "wss://ws.deriv.com/websockets/v3?app_id=1089",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()