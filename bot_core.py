import websocket
import json
import time
import threading

# Função principal
def iniciar_robo(token, stake, martingale, stop_loss, take_profit, delay, analise_ticks):
    saldo = 0.0
    perdas_consecutivas = 0
    ws_url = "wss://ws.deriv.com/websockets/v3?app_id=1089"
    running = True

    def on_message(ws, message):
        nonlocal saldo, perdas_consecutivas, running
        data = json.loads(message)

        # Processa msg_type
        if data.get('msg_type') == 'authorize':
            print("✅ Autorizado com sucesso.")
            requisitar_ticks(ws, analise_ticks)
        elif data.get('msg_type') == 'history':
            # Extrai últimos digits
            ticks = data['history']['prices'][-analise_ticks:]
            ultimos_digitos = [int(t[-1]) for t in ticks]
            print(f"📊 Últimos dígitos: {ultimos_digitos}")
            baixo_4 = sum(1 for d in ultimos_digitos if d < 4)
            print(f"🧮 Dígitos <4: {baixo_4} de {analise_ticks}")
            # Se >= 60%, aposta Over 3
            if baixo_4 >= int(analise_ticks * 0.6):
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
                    "passthrough": {"info": "Predador de Padrões"},
                    "req_id": 1
                }
                print("🎯 Padrão detectado! Enviando entrada Over 3...")
                ws.send(json.dumps(contrato))
            else:
                print("⏸️ Padrão não favorável. Aguardando próximo ciclo...")
                time.sleep(delay)
                requisitar_ticks(ws, analise_ticks)
        elif data.get('msg_type') == 'buy':
            print("🟡 Entrada enviada. Aguardando resultado...")
        elif data.get('msg_type') == 'proposal_open_contract':
            if data['proposal_open_contract']['is_sold']:
                profit = float(data['proposal_open_contract']['profit'])
                resultado = "WIN" if profit > 0 else "LOSS"
                saldo += profit
                print(f"📈 Resultado: {resultado} | Lucro: {profit:.2f} | Saldo Total: {saldo:.2f}")
                # Controle de perdas
                if resultado == "LOSS":
                    perdas_consecutivas += 1
                else:
                    perdas_consecutivas = 0
                # Verifica stop loss ou meta
                if saldo <= -stop_loss or perdas_consecutivas >= 4:
                    print("🛑 Stop atingido. Encerrando robô.")
                    ws.close()
                    return
                if saldo >= take_profit:
                    print("🎯 Meta de lucro atingida. Encerrando robô.")
                    ws.close()
                    return
                time.sleep(delay)
                requisitar_ticks(ws, analise_ticks)
        # Outros msg_type podem ser ignorados

    def on_error(ws, error):
        print(f"❌ Erro: {error}")
    def on_close(ws, close_status_code, close_msg):
        print("🔌 Conexão encerrada.")
    def on_open(ws):
        print("🟢 Conectando e autenticando...")
        auth = {"authorize": token}
        ws.send(json.dumps(auth))

    def requisitar_ticks(ws, analise_ticks):
        msg = {
            "ticks_history": "R_100",
            "adjust_start_time": 1,
            "count": analise_ticks,
            "end": "latest",
            "start": 1,
            "style": "ticks"
        }
        ws.send(json.dumps(msg))

    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()