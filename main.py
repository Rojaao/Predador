import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    token = st.text_input("🎯 Insira seu Token da Deriv")
    stake = st.number_input("💰 Stake Inicial", value=1.0)
    fator_martingale = st.number_input("📈 Fator Martingale", value=2.0)
    estrategia = st.selectbox("🎯 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])

    placeholder_log = st.empty()

    if st.button("🚀 Iniciar Robô"):
        placeholder_log.markdown("```text\n🔌 Iniciando conexão com a Deriv...\n```")
        iniciar_conexao(token, stake, fator_martingale, estrategia, placeholder_log)