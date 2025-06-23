import websocket
import json
import threading
import time
import queue
from estrategias import predador_de_padroes, identificador_de_padrao
from utils import som_sucesso, som_erro

LOG_QUEUE = queue.Queue()

def iniciar_conexao(token, stake, martingale, fator, stop_loss, stop_gain, strategy, atualizar_status):
    ws_url = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
    bot = BotDeriv(token, stake, martingale, fator, stop_loss, stop_gain, strategy, atualizar_status)
    bot.start(ws_url)

class BotDeriv:
    def __init__(self, token, stake, martingale, fator, stop_loss, stop_gain, strategy, atualizar_status):
        self.token = token
        self.stake_inicial = stake
        self.stake = stake
        self.martingale = martingale
        self.fator = fator
        self.stop_loss = stop_loss
        self.stop_gain = stop_gain
        self.strategy = strategy  # 'predador' ou 'identificador'
        self.atualizar_status = atualizar_status
        self.saldo = 0.0
        self.lucro = 0.0
        self.perdas_seguidas = 0
        self.ws = None
        self.running = True
        self.lock = threading.Lock()

    def log(self, msg):
        timestamp = time.strftime('%H:%M:%S')
        full = f'[{timestamp}] {msg}'
        try:
            self.atualizar_status(full)
        except Exception:
            pass

    def start(self, ws_url):
        self.ws = websocket.WebSocketApp(
            ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        thread.start()

    def on_open(self, ws):
        self.log("Conectando à Deriv...")
        auth = {"authorize": self.token}
        ws.send(json.dumps(auth))

    def on_message(self, ws, message):
        data = json.loads(message)
        msg_type = data.get("msg_type")
        if msg_type == "authorize":
            if data.get("error"):
                self.log(f"Erro na autenticação: {data['error']['message']}")
                self.running = False
                ws.close()
                return
            self.log("Autenticado com sucesso.")
            # solicita balance
            ws.send(json.dumps({"balance":1}))
            # solicita primeiro ticks
            self.request_ticks(ws)
        elif msg_type == "balance":
            # balance retornado em cents, ex: 10000 = $100
            bal = data["balance"]["balance"]
            self.saldo = bal/100.0
            self.log(f"Saldo inicial: ${self.saldo:.2f}")
        elif msg_type == "history":
            # coleta de ticks: data["history"]["prices"] é dict index->value ou list
            prices = data["history"].get("prices", [])
            # extrai últimos 10 dígitos
            digitos = []
            if isinstance(prices, dict):
                vals = list(prices.values())
                digitos = [int(str(v)[-1]) for v in vals[-10:]]
            elif isinstance(prices, list):
                digitos = [int(str(v)[-1]) for v in prices[-10:]]
            self.log(f"Últimos 10 dígitos: {digitos}")
            # estratégia
            if self.strategy == 'predador':
                ok = predador_de_padroes(digitos)
            else:
                # identificador precisa function send_request_func: define aqui
                def send_request():
                    # envia request e aguarda resposta síncrona
                    ev = threading.Event()
                    result = []
                    def on_hist(ws, msg):
                        d = json.loads(msg)
                        if d.get('msg_type')=='history':
                            vals = d['history'].get('prices', [])
                            if isinstance(vals, dict):
                                arr = [int(str(v)[-1]) for v in list(vals.values())[-10:]]
                            else:
                                arr = [int(str(v)[-1]) for v in vals[-10:]]
                            result.extend(arr)
                            ev.set()
                    # temporariamente registra callback
                    orig = self.ws.on_message
                    self.ws.on_message = on_hist
                    self.ws.send(json.dumps({
                        "ticks_history":"R_100","adjust_start_time":1,
                        "count":10,"end":"latest","style":"ticks"
                    }))
                    ev.wait(timeout=10)
                    # restaura on_message
                    self.ws.on_message = orig
                    return result
                ok = identificador_de_padrao(send_request, self.log)
            if ok:
                self.log("Padrão favorável detectado! Enviando ordem Over 3.")
                self.send_order(ws)
            else:
                self.log("Padrão não favorável. Aguardando próximo ciclo.")
                time.sleep(2)
                self.request_ticks(ws)
        elif msg_type == "buy":
            # confirmação de envio de ordem
            self.log("Ordem enviada, aguardando resultado...")
        elif msg_type == "proposal_open_contract":
            poc = data["proposal_open_contract"]
            profit = float(poc.get("profit", 0))
            status = "WIN" if profit>0 else "LOSS"
            self.lucro += profit
            self.log(f"Resultado da operação: {status}, Profit: {profit:.2f}, Lucro acumulado: {self.lucro:.2f}")
            if status=="LOSS":
                self.perdas_seguidas +=1
                if self.martingale:
                    self.stake *= self.fator
                    self.log(f"Aplicando Martingale. Nova stake: {self.stake:.2f}")
            else:
                self.perdas_seguidas = 0
                self.stake = self.stake_inicial
            # checa stop_loss/gain
            if self.lucro <= -abs(self.stop_loss):
                self.log("Stop Loss atingido. Parando robô.")
                self.running=False
                ws.close()
                return
            if self.lucro >= abs(self.stop_gain):
                self.log("Stop Gain atingido. Parando robô.")
                self.running=False
                ws.close()
                return
            # próximo ciclo
            time.sleep(2)
            self.request_ticks(ws)
        # outros msg_types ignorados

    def request_ticks(self, ws):
        ws.send(json.dumps({"ticks_history":"R_100","adjust_start_time":1,"count":10,"end":"latest","style":"ticks"}))

    def send_order(self, ws):
        ws.send(json.dumps({
            "buy":1,"price": round(self.stake, 2),
            "parameters":{
                "amount": round(self.stake, 2),
                "basis":"stake","contract_type":"DIGITOVER",
                "currency":"USD","duration":1,"duration_unit":"t","symbol":"R_100","barrier":3
            }
        }))

    def on_error(self, ws, error):
        self.log(f"Erro WebSocket: {error}")
        # Em caso de erro de DNS, log e parar
        if "Name or service not known" in str(error):
            self.log("Erro de DNS: verifique URL ou ambiente.")
            self.running=False
            ws.close()

    def on_close(self, ws, close_status_code=None, close_msg=None):
        self.log("Conexão WebSocket fechada.")