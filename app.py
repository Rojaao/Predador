
import streamlit as st
from bot_core import iniciar_robo

st.set_page_config(page_title="Predador de Padrões - por Rogger", layout="centered")
st.title("🧠 Predador de Padrões")
st.markdown("**por Rogger**")

token = st.text_input("🔑 Insira seu token da Deriv (demo ou real)", type="password")
stake = st.number_input("💰 Stake inicial (R$)", min_value=0.35, value=1.00, step=0.01)
martingale = st.number_input("🎯 Fator de Martingale", min_value=1.0, value=2.0, step=0.1)
stop_loss = st.number_input("⛔ Stop Loss (R$)", min_value=1.0, value=60.0)
take_profit = st.number_input("✅ Meta de Lucro (R$)", min_value=1.0, value=50.0)
delay = st.slider("⏱️ Delay entre entradas (segundos)", 1, 30, 7)
analise_ticks = st.selectbox("📊 Analisar quantos últimos dígitos?", [10, 20, 50])

if st.button("▶️ Iniciar Robô"):
    if token:
        iniciar_robo(token, stake, martingale, stop_loss, take_profit, delay, analise_ticks)
    else:
        st.warning("Por favor, insira um token válido.")
