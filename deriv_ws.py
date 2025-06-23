
import websocket
import threading
import time
import json
from estrategias import predador_de_padroes, identificador_de_padrao
from utils import simular_digitos, simular_coletas

def iniciar_conexao(token, stake, usar_martingale, fator_martingale, stop_loss, stop_gain, estrategia, atualizar_interface):
    def on_open(ws):
        atualizar_interface("✅ Conexão estabelecida com a Deriv!")
        ws.send(json.dumps({
            "authorize": token
        }))
        rodar_estrategia(ws)

    def on_message(ws, message):
        print("📩 Mensagem recebida:", message)

    def on_error(ws, error):
        atualizar_interface(f"❌ Erro: {error}")

    def on_close(ws, *args):
        atualizar_interface("🔌 Conexão encerrada.")

    def rodar_estrategia(ws):
        while True:
            if estrategia == "Predador de Padrões":
                digitos = simular_digitos()
                decisao = predador_de_padroes(digitos)
                atualizar_interface(f"📊 Últimos dígitos: {digitos} -> Decisão: {decisao}")
            elif estrategia == "Identificador de Padrão":
                coletas = simular_coletas()
                decisao = identificador_de_padrao(coletas)
                atualizar_interface(f"📊 Coletas: {coletas} -> Decisão: {decisao}")
            time.sleep(5)

    ws = websocket.WebSocketApp(
        "wss://ws.derivws.com/websockets/v3",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    thread = threading.Thread(target=ws.run_forever)
    thread.start()
