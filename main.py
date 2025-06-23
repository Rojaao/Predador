import streamlit as st
from deriv_ws import iniciar_conexao

log_box = None

def atualizar_interface(msg):
    global log_box
    if log_box:
        log_box.markdown("```text\n{}\n```".format(msg))

def main():
    global log_box
    st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    token = st.text_input("🔑 Insira seu Token da Deriv", type="password")
    stake = st.number_input("💰 Stake inicial", min_value=0.35, value=1.00)
    martingale = st.checkbox("🎯 Ativar Martingale")
    estrategia = st.selectbox("📊 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    iniciar = st.button("🚀 Iniciar Robô")

    log_box = st.empty()

    if iniciar and token:
        atualizar_interface("🔌 Iniciando conexão com a Deriv...")
        iniciar_conexao(token, stake, martingale, estrategia, atualizar_interface)