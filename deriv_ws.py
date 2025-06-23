
import websocket
import json
import threading
import time
from estrategias import predador_de_padroes, identificador_de_padrao

digitos_recentes = []
coletas = []

def iniciar_conexao(token, stake, martingale, fator, estrategia_func, atualizar_interface):
    def on_message(ws, message):
        global digitos_recentes, coletas

        data = json.loads(message)
        if "msg_type" in data and data["msg_type"] == "history":
            ultimos = [int(c[-1]) for c in data["history"]["prices"][-10:]]
            digitos_recentes = ultimos

            if estrategia_func == identificador_de_padrao:
                coletas.append(ultimos)
                if len(coletas) > 3:
                    coletas.pop(0)
                padrao = estrategia_func(coletas)
            else:
                padrao = estrategia_func(digitos_recentes)

            if padrao:
                atualizar_interface("🎯 Padrão detectado! Enviando entrada Over 3...")
                enviar_ordem(ws, stake)
            else:
                atualizar_interface(f"⏸️ Aguardando padrão... Últimos dígitos: {digitos_recentes}")

    def enviar_ordem(ws, stake):
        buy = {
            "buy": 1,
            "price": stake,
            "parameters": {
                "amount": stake,
                "basis": "stake",
                "contract_type": "DIGITOVER",
                "barrier": "3",
                "currency": "USD",
                "duration": 1,
                "duration_unit": "t",
                "symbol": "R_100"
            },
            "passthrough": {"ref": "digit"},
            "req_id": 1
        }
        ws.send(json.dumps(buy))

    def on_open(ws):
        ws.send(json.dumps({"authorize": token}))
        ws.send(json.dumps({
            "ticks_history": "R_100",
            "adjust_start_time": 1,
            "count": 100,
            "end": "latest",
            "start": 1,
            "style": "ticks",
            "subscribe": 1
        }))

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws, *args):
        atualizar_interface("🔌 Conexão encerrada.")

    def run():
        ws.run_forever()

    ws = websocket.WebSocketApp(
        "wss://ws.binaryws.com/websockets/v3?app_id=1089",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    threading.Thread(target=run).start()
