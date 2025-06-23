import websocket
import json
import time

def iniciar_robo(token, stake, martingale, stop_loss, take_profit, delay, analise_ticks):
    saldo = 0.0
    perdas_consecutivas = 0
    # Endpoint corrigido para Deriv WebSocket
    ws_url = "wss://ws.binaryws.com/websockets/v3?app_id=1089"

    def on_open(ws):
        print("🟢 Conectando ao WebSocket da Deriv...")
        auth = {"authorize": token}
        ws.send(json.dumps(auth))

    def on_message(ws, message):
        nonlocal saldo, perdas_consecutivas
        data = json.loads(message)
        # Debug de mensagem recebida
        print("📩 Mensagem recebida:", data.get("msg_type", data))

        if data.get("msg_type") == "authorize":
            if data.get("authorize", {}).get("error"):
                print("❌ Autorização falhou:", data["authorize"]["error"]["message"])
                ws.close()
                return
            print("✅ Autorizado com sucesso.")
            # Solicita ticks iniciais
            requisitar_ticks(ws, analise_ticks)

        elif data.get("msg_type") == "history":
            # Extrai últimos ticks
            prices = data.get("history", {}).get("prices", [])
            if not prices:
                print("⚠️ Histórico vazio recebido, tentando novamente...")
                time.sleep(delay)
                requisitar_ticks(ws, analise_ticks)
                return
            # Cada item de prices pode ser string ou dict, dependendo da resposta
            # Se for string, último caractere é o dígito final
            ultimos_digitos = []
            for t in prices[-analise_ticks:]:
                # t pode ser número ou string: convertendo para str
                s = str(t)
                # último caractere
                try:
                    d = int(s[-1])
                except:
                    continue
                ultimos_digitos.append(d)
            print(f"📊 Últimos dígitos ({len(ultimos_digitos)}): {ultimos_digitos}")
            baixo_4 = sum(1 for d in ultimos_digitos if d < 4)
            print(f"🧮 Dígitos <4: {baixo_4} de {analise_ticks}")
            # Critério: se ≥ 60% abaixo de 4, entra Over 3
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

        elif data.get("msg_type") == "buy":
            print("🟡 Entrada enviada. Aguardando resultado...")

        elif data.get("msg_type") == "proposal_open_contract":
            # Verifica se a proposta foi vendida (fechada)
            porc = data.get("proposal_open_contract", {})
            if porc.get("is_sold"):
                profit = float(porc.get("profit", 0))
                resultado = "WIN" if profit > 0 else "LOSS"
                saldo += profit
                print(f"📈 Resultado: {resultado} | Lucro: {profit:.2f} | Saldo Total: {saldo:.2f}")
                # Controle de perdas consecutivas
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

    def on_error(ws, error):
        print(f"❌ Erro na conexão/WebSocket: {error}")
        # Aqui você pode implementar reconexão ou encerrar
        ws.close()

    def on_close(ws, close_status_code, close_msg):
        print("🔌 Conexão encerrada com a Deriv.")

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
    try:
        ws.run_forever()
    except Exception as e:
        print("❌ Exceção em run_forever:", e)
        ws.close()
