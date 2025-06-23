import websocket
import json
import time
from estrategias import predador_de_padroes, identificador_de_padrao

def iniciar_conexao(token, stake, usar_martingale, estrategia, atualizar_interface):
    url = "wss://ws.derivws.com/websockets/v3?app_id=1089"

    def on_open(ws):
        ws.send(json.dumps({
            "authorize": token
        }))
        atualizar_interface("✅ Conectado à Deriv.")

    def on_message(ws, message):
        data = json.loads(message)
        if 'msg_type' in data and data['msg_type'] == 'authorize':
            ws.send(json.dumps({
                "ticks": "R_100"
            }))
        elif data.get("msg_type") == "tick":
            ultimo_digito = int(str(data["tick"]["quote"])[-1])
            atualizar_interface(f"📊 Último dígito: {ultimo_digito}")

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws, *args):
        atualizar_interface("🔌 Conexão encerrada.")

    def run():
        ws = websocket.WebSocketApp(
            url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.run_forever()

    run()