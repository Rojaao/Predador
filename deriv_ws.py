import websocket
import json
import threading
import time
from estrategias import predador_de_padroes
from utils import som_sucesso, som_erro

def iniciar_conexao(token, stake, martingale, fator, stop_loss, stop_gain, atualizar_interface):
    ws_url = "wss://ws.deriv.com/websockets/v3"
    saldo = 0
    lucro = 0
    historico = []
    em_operacao = False
    ultima_stake = stake
    perdas_seguidas = 0

    def enviar_tick_history():
        ws.send(json.dumps({
            "ticks_history": "R_100",
            "adjust_start_time": 1,
            "count": 10,
            "end": "latest",
            "style": "digits",
            "granularity": 1,
            "subscribe": 1,
            "req_id": "1"
        }))

    def enviar_ordem():
        nonlocal em_operacao
        em_operacao = True
        buy = {
            "buy": 1,
            "price": round(ultima_stake, 2),
            "parameters": {
                "amount": round(ultima_stake, 2),
                "basis": "stake",
                "contract_type": "DIGITOVER",
                "currency": "USD",
                "duration": 1,
                "duration_unit": "t",
                "symbol": "R_100",
                "barrier": "3"
            },
            "req_id": "2"
        }
        ws.send(json.dumps(buy))
        atualizar_interface("🎯 Entrada enviada com stake $" + str(round(ultima_stake, 2)))

    def on_message(ws, message):
        nonlocal saldo, lucro, em_operacao, ultima_stake, perdas_seguidas
        msg = json.loads(message)

        if "msg_type" not in msg:
            return

        if msg["msg_type"] == "authorize":
            atualizar_interface("✅ Conectado com sucesso à Deriv!")
            ws.send(json.dumps({"balance": 1, "req_id": "balance"}))
            enviar_tick_history()

        elif msg["msg_type"] == "balance":
            saldo = msg["balance"]["balance"]
            atualizar_interface(f"💰 Saldo: ${saldo/100:.2f}")

        elif msg["msg_type"] == "history":
            ultimos = [int(d) for d in msg["history"]["prices"].values()]
            atualizar_interface(f"📊 Últimos dígitos: {ultimos}")
            if predador_de_padroes(ultimos):
                atualizar_interface("🔍 Padrão identificado!")
                enviar_ordem()

        elif msg["msg_type"] == "buy":
            atualizar_interface("⏳ Ordem enviada, aguardando resultado...")

        elif msg["msg_type"] == "proposal_open_contract":
            status = msg["proposal_open_contract"]["status"]
            if status == "won":
                atualizar_interface("✅ Vitória! Lucro registrado.")
                som_sucesso()
                lucro += float(msg["proposal_open_contract"]["profit"])
                ultima_stake = stake
                perdas_seguidas = 0
            elif status == "lost":
                atualizar_interface("❌ Derrota! Aplicando martingale.")
                som_erro()
                lucro -= float(msg["proposal_open_contract"]["buy_price"])
                perdas_seguidas += 1
                if martingale:
                    ultima_stake *= fator
            atualizar_interface(f"📈 Lucro acumulado: ${lucro:.2f}")
            if lucro <= -abs(stop_loss):
                atualizar_interface("🛑 Stop Loss atingido.")
                ws.close()
            elif lucro >= abs(stop_gain):
                atualizar_interface("🎯 Stop Gain alcançado!")
                ws.close()
            else:
                em_operacao = False
                time.sleep(3)
                enviar_tick_history()

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws):
        atualizar_interface("🔌 Conexão encerrada.")

    def on_open(ws):
        ws.send(json.dumps({"authorize": token}))

    def run():
        ws.run_forever()

    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    thread = threading.Thread(target=run)
    thread.start()