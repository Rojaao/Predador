import websocket
import json
import threading
import time
from estrategias import predador_de_padroes

def iniciar_conexao(token, stake, martingale, fator_martingale, stop_loss, stop_gain, atualizar_interface):
    ws_url = "wss://ws.deriv.com/websockets/v3?app_id=1089"
    ws = websocket.WebSocketApp(ws_url,
                                 on_open=lambda ws: on_open(ws, token),
                                 on_message=lambda ws, msg: on_message(ws, msg, stake, martingale, fator_martingale, stop_loss, stop_gain, atualizar_interface),
                                 on_error=lambda ws, err: atualizar_interface({'log': f"❌ Erro: {err}"}),
                                 on_close=lambda ws: atualizar_interface({'log': "🔌 Conexão encerrada."}))

    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()

def on_open(ws, token):
    auth_req = {"authorize": token}
    ws.send(json.dumps(auth_req))

def on_message(ws, message, stake, martingale, fator_martingale, stop_loss, stop_gain, atualizar_interface):
    msg = json.loads(message)
    if msg.get("msg_type") == "authorize":
        atualizar_interface({'log': "🔑 Autenticado com sucesso!"})
        ws.send(json.dumps({"ticks_history": "R_100", "adjust_start_time": 1, "count": 100, "end": "latest", "style": "ticks", "subscribe": 1}))

    elif msg.get("msg_type") == "history":
        ultimos_digitos = [int(str(d)[-1]) for d in msg["history"]["prices"][-10:]]
        qtd_menores_que_4 = sum(1 for d in ultimos_digitos if d < 4)

        atualizar_interface({'log': f"📊 Últimos dígitos (10): {ultimos_digitos}\n🧮 Dígitos <4: {qtd_menores_que_4} de 10"})

        if predador_de_padroes(ultimos_digitos):
            atualizar_interface({'log': "🎯 Padrão detectado! Enviando entrada Over 3..."})
            proposal = {
                "buy": 1,
                "price": stake,
                "parameters": {
                    "amount": stake,
                    "basis": "stake",
                    "contract_type": "DIGITOVER",
                    "duration": 1,
                    "duration_unit": "t",
                    "symbol": "R_100",
                    "barrier": 3
                }
            }
            ws.send(json.dumps(proposal))