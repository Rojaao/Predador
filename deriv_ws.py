
import threading
import websocket

def iniciar_conexao(token, estrategia, stake, martingale, placeholder_log):
    def on_message(ws, message):
        placeholder_log.markdown(f"```text\n📩 Mensagem recebida: {message}\n```")

    def on_error(ws, error):
        placeholder_log.markdown(f"```text\n❌ Erro: {error}\n```")

    def on_close(ws, close_status_code=None, close_msg=None):
        placeholder_log.markdown("```text\n🔌 Conexão encerrada.\n```")

    def on_open(ws):
        placeholder_log.markdown("```text\n✅ Conexão estabelecida com a Deriv!\n```")

    ws = websocket.WebSocketApp(
        "wss://ws.binaryws.com/websockets/v3?app_id=1089",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open
    )

    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
