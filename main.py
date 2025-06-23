
import streamlit as st
from deriv_ws import iniciar_conexao

st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")

log_box = st.empty()

def atualizar_interface(msg):
    log_box.markdown("```text\n{}\n```".format(msg))

def main():
    st.title("🤖 Robô Predador de Padrões")
    token = st.text_input("🔑 Token da Deriv", type="password")
    estrategia = st.selectbox("🎯 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    stake = st.number_input("💰 Stake inicial", min_value=0.35, value=1.00, step=0.01)
    martingale = st.checkbox("🎲 Ativar Martingale")
    fator_martingale = st.number_input("📈 Fator Martingale", min_value=1.0, value=2.0, step=0.1)
    stop_loss = st.number_input("🛑 Stop Loss", min_value=1.0, value=20.0, step=1.0)
    stop_gain = st.number_input("🎯 Stop Gain", min_value=1.0, value=20.0, step=1.0)

    if st.button("🚀 Iniciar Robô"):
        atualizar_interface("🔌 Iniciando conexão com a Deriv...")
        iniciar_conexao(
            token=token,
            stake=stake,
            usar_martingale=martingale,
            fator_martingale=fator_martingale,
            stop_loss=stop_loss,
            stop_gain=stop_gain,
            estrategia=estrategia,
            atualizar_interface=atualizar_interface
        )

