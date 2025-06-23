
import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    token = st.text_input("🔑 Token da API Deriv", type="password")
    estrategia = st.selectbox("🎯 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    stake = st.number_input("💰 Stake Inicial", value=1.0)
    martingale = st.checkbox("🎲 Ativar Martingale", value=True)

    placeholder_log = st.empty()

    if st.button("🚀 Iniciar Robô"):
        placeholder_log.markdown("```text\nIniciando conexão com a Deriv...\n```")
        iniciar_conexao(token, estrategia, stake, martingale, placeholder_log)
