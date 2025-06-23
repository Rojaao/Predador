import websocket
import json
import threading
import time
from estrategias import predador_de_padroes, identificador_padrao

def iniciar_conexao(token, stake, estrategia, martingale, fila_logs):
    def enviar(msg): 
        ws.send(json.dumps(msg))

    def on_open(ws):
        fila_logs.put("🔌 Conectando à Deriv...")
        enviar({"authorize": token})

    def on_message(ws, message):
        dados = json.loads(message)
        fila_logs.put(f"📩 Mensagem recebida: {dados.get('msg_type', 'desconhecida')}")

        if dados.get("msg_type") == "authorize":
            fila_logs.put("✅ Autorizado com sucesso!")
            if estrategia == "Predador de Padrões":
                threading.Thread(target=predador_de_padroes, args=(ws, stake, martingale, fila_logs)).start()
            elif estrategia == "Identificador de Padrão":
                threading.Thread(target=identificador_padrao, args=(ws, stake, martingale, fila_logs)).start()

    def on_error(ws, error):
        fila_logs.put(f"❌ Erro: {error}")

    def on_close(ws, *args):
        fila_logs.put("🔌 Conexão encerrada.")

    ws = websocket.WebSocketApp(
        "wss://ws.binaryws.com/websockets/v3?app_id=1089",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    threading.Thread(target=ws.run_forever).start()