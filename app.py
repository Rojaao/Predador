import streamlit as st
import threading
from bot_core import iniciar_robo

st.set_page_config(page_title="Predador de Padrões", layout="centered")
st.title("🧠 Predador de Padrões")
st.markdown("**Interface para Predador de Padrões - Over 3 (1 tick)**")

# Inicialização do estado
if "thread" not in st.session_state:
    st.session_state.thread = None
if "running" not in st.session_state:
    st.session_state.running = False

token = st.text_input("🔑 Insira seu token da Deriv (demo ou real)", type="password")
stake = st.number_input("💰 Stake inicial (USD)", min_value=0.35, value=1.00, step=0.01)
martingale = st.number_input("🎯 Fator de Martingale", min_value=1.0, value=2.0, step=0.1)
stop_loss = st.number_input("⛔ Stop Loss (USD)", min_value=1.0, value=60.0)
take_profit = st.number_input("✅ Meta de Lucro (USD)", min_value=1.0, value=50.0)
delay = st.slider("⏱️ Delay entre entradas (segundos)", 1, 120, 7)
analise_ticks = st.selectbox("📊 Analisar quantos últimos dígitos?", [10, 20, 50])

status_placeholder = st.empty()
log_placeholder = st.empty()

def run_bot():
    iniciar_robo(token, stake, martingale, stop_loss, take_profit, delay, analise_ticks)

col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Iniciar Robô") and not st.session_state.running:
        if not token:
            st.warning("⚠️ Insira um token válido.")
        else:
            st.session_state.running = True
            status_placeholder.info("🚀 Rodando... Veja logs no console.")
            # Iniciar thread para o robô
            st.session_state.thread = threading.Thread(target=run_bot, daemon=True)
            st.session_state.thread.start()
with col2:
    if st.button("⛔ Parar Robô") and st.session_state.running:
        st.session_state.running = False
        status_placeholder.info("⏸️ Parado")
        # Nota: o bot_core deve verificar st.session_state.running para parar

# Instrução para o usuário
st.markdown("### 🔍 Logs e status")
st.markdown("- Os logs de conexão e operações aparecerão no console do servidor (Render ou local).")
st.markdown("- Para ver se está conectando, consulte os logs do serviço.")