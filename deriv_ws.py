import websocket
import json
import threading
from estrategias import predador_de_padroes, identificador_de_padrao

def iniciar_conexao(token, estrategia, atualizar_interface):
    def on_open(ws):
        atualizar_interface("✅ Conexão estabelecida com a Deriv!")
        auth_data = json.dumps({"authorize": token})
        ws.send(auth_data)

    def on_message(ws, message):
        dados = json.loads(message)
        if 'msg_type' in dados:
            if dados['msg_type'] == 'authorize':
                ws.send(json.dumps({
                    "ticks_history": "R_100",
                    "adjust_start_time": 1,
                    "count": 100,
                    "end": "latest",
                    "start": 1,
                    "style": "ticks",
                    "subscribe": 1
                }))
            elif dados['msg_type'] == 'history':
                ultimos_ticks = dados['history']['prices']
                if estrategia == "Predador de Padrões":
                    predador_de_padroes(ultimos_ticks, ws, token)
                elif estrategia == "Identificador de Padrão":
                    identificador_de_padrao(ultimos_ticks, ws, token)

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws, *args):
        atualizar_interface("🔌 Conexão encerrada.")

    def run():
        ws_app = websocket.WebSocketApp(
            "wss://ws.binaryws.com/websockets/v3?app_id=1089",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws_app.run_forever()

    thread = threading.Thread(target=run)
    thread.start()
