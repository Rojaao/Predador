import websocket
import json

def iniciar_conexao(token, stake, martingale, estrategia):
    print("🔌 Conectando à Deriv...")
    # Aqui seria onde você conecta via WebSocket