
import websocket
import json
import time
import threading
import streamlit as st
from datetime import datetime

def iniciar_robo(token, stake, martingale, stop_loss, take_profit, delay, analise_ticks):
    saldo = st.session_state.lucro_total
    perdas_consecutivas = 0
    ws_url = "wss://ws.deriv.com/websockets/v3?app_id=1089"
    contrato_em_andamento = False

    def on_message(ws, message):
        nonlocal saldo, perdas_consecutivas, contrato_em_andamento

        if st.session_state.parar:
            print("⛔ Parada manual detectada. Encerrando...")
            ws.close()
            return

        data = json.loads(message)

        if 'msg_type' in data:
            if data['msg_type'] == 'history' and not contrato_em_andamento:
                ultimos_digitos = [int(str(tick)[-1]) for tick in data['history']['prices'][-analise_ticks:]]
                baixo_4 = sum(1 for d in ultimos_digitos if d < 4)

                if baixo_4 >= int(analise_ticks * 0.6):
                    contrato_em_andamento = True
                    contrato = {
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
                    ws.send(json.dumps(contrato))

            elif data['msg_type'] == 'buy':
                print("🎯 Entrada enviada com sucesso. Aguardando resultado...")

            elif data['msg_type'] == 'proposal_open_contract':
                if data['proposal_open_contract']['is_sold']:
                    profit = float(data['proposal_open_contract']['profit'])
                    resultado = "WIN" if profit > 0 else "LOSS"
                    saldo += profit
                    st.session_state.lucro_total = saldo

                    agora = datetime.now().strftime("%H:%M:%S")
                    st.session_state.historico.append({
                        "Horário": agora,
                        "Resultado": resultado,
                        "Lucro": f"${profit:.2f}"
                    })

                    if resultado == "WIN":
                        st.audio("win.mp3", format="audio/mp3", start_time=0)
                        perdas_consecutivas = 0
                    else:
                        st.audio("loss.mp3", format="audio/mp3", start_time=0)
                        perdas_consecutivas += 1

                    contrato_em_andamento = False

                    if saldo <= -stop_loss or perdas_consecutivas >= 4:
                        st.session_state.status = "⛔ Stop atingido"
                        ws.close()
                        return

                    if saldo >= take_profit:
                        st.session_state.status = "🎯 Meta atingida"
                        ws.close()
                        return

                    time.sleep(delay)
                    requisitar_ticks()

    def on_error(ws, error):
        print(f"Erro: {error}")

    def on_close(ws, close_status_code, close_msg):
        print("🔌 Conexão encerrada.")

    def on_open(ws):
        print("🟢 Conectado com sucesso.")
        auth = {"authorize": token}
        ws.send(json.dumps(auth))
        threading.Thread(target=requisitar_ticks).start()

    def requisitar_ticks():
        ticks_msg = {
            "ticks_history": "R_100",
            "adjust_start_time": 1,
            "count": analise_ticks,
            "end": "latest",
            "start": 1,
            "style": "ticks"
        }
        ws.send(json.dumps(ticks_msg))

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()
