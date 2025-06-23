
import websocket
import json
import time
import threading

def iniciar_robo(token, stake, martingale, stop_loss, take_profit, delay, analise_ticks):
    saldo = 0
    perdas_consecutivas = 0
    ws_url = "wss://ws.deriv.com/websockets/v3?app_id=1089"

    def on_message(ws, message):
        nonlocal saldo, perdas_consecutivas

        data = json.loads(message)

        if 'msg_type' in data:
            if data['msg_type'] == 'history':
                ultimos_digitos = [int(tick['quote'][-1]) for tick in data['history']['prices'][-analise_ticks:]]
                baixo_4 = sum(1 for d in ultimos_digitos if d < 4)

                if baixo_4 >= int(analise_ticks * 0.6):
                    print(f"🔥 Padrão detectado ({baixo_4} dígitos < 4). Enviando entrada OVER 3...")

                    contract = {
                        "buy": 1,
                        "price": stake,
                        "parameters": {
                            "amount": stake,
                            "basis": "stake",
                            "contract_type": "DIGITOVER",
                            "currency": "USD",
                            "duration": 1,
                            "duration_unit": "t",
                            "symbol": "R_100",
                            "barrier": "3"
                        },
                        "passthrough": {"info": "Predador de Padroes"},
                        "req_id": 1
                    }
                    ws.send(json.dumps(contract))

            elif data['msg_type'] == 'buy':
                print("🟡 Entrada enviada com sucesso. Aguardando resultado...")

            elif data['msg_type'] == 'proposal_open_contract':
                if data['proposal_open_contract']['is_sold']:
                    profit = float(data['proposal_open_contract']['profit'])
                    saldo += profit
                    resultado = "✅ WIN" if profit > 0 else "❌ LOSS"
                    print(f"{resultado} | Lucro: {profit:.2f} | Saldo total: {saldo:.2f}")
                    if profit < 0:
                        perdas_consecutivas += 1
                        if saldo <= -stop_loss or perdas_consecutivas >= 4:
                            print("🛑 Stop atingido. Robô pausado.")
                            ws.close()
                            return
                    else:
                        perdas_consecutivas = 0
                    if saldo >= take_profit:
                        print("🎯 Meta de lucro atingida! Robô finalizado.")
                        ws.close()
                        return
                    time.sleep(delay)
                    requisitar_tempo_real()

    def on_error(ws, error):
        print(f"Erro na conexão: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("🔌 Conexão encerrada.")

    def on_open(ws):
        print("🟢 Conectado com sucesso. Robô operando...")
        auth = {"authorize": token}
        ws.send(json.dumps(auth))

        def run_logic():
            requisitar_tempo_real()

        threading.Thread(target=run_logic).start()

    def requisitar_tempo_real():
        ticks_msg = {
            "ticks_history": "R_100",
            "adjust_start_time": 1,
            "count": analise_ticks,
            "end": "latest",
            "start": 1,
            "style": "ticks"
        }
        ws.send(json.dumps(ticks_msg))

    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
