import json
import time

def predador_de_padroes(ws, stake, atualizar_interface):
    atualizar_interface("📊 Estratégia 'Predador de Padrões' iniciada.")
    contract = {
        "buy": 1,
        "price": stake,
        "parameters": {
            "amount": stake,
            "basis": "stake",
            "contract_type": "CALL",
            "currency": "USD",
            "duration": 1,
            "duration_unit": "t",
            "symbol": "R_100"
        }
    }
    ws.send(json.dumps(contract))

def nova_estrategia(ws, stake, atualizar_interface):
    atualizar_interface("🧠 Estratégia 'Nova Estratégia' em execução.")
    contract = {
        "buy": 1,
        "price": stake,
        "parameters": {
            "amount": stake,
            "basis": "stake",
            "contract_type": "PUT",
            "currency": "USD",
            "duration": 1,
            "duration_unit": "t",
            "symbol": "R_100"
        }
    }
    ws.send(json.dumps(contract))