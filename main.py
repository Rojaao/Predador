import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    token = st.text_input("🔑 Insira seu token da Deriv", type="password")
    estrategia = st.selectbox("🎯 Escolha a estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    stake = st.number_input("💰 Stake inicial", min_value=0.35, value=1.00)
    martingale = st.checkbox("📈 Ativar Martingale")

    iniciar = st.button("🚀 Iniciar Robô")

    if iniciar and token:
        st.success("🔌 Iniciando conexão com a Deriv...")
        iniciar_conexao(token, stake, martingale, estrategia)