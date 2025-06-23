import streamlit as st
from deriv_ws import iniciar_conexao

log_box = None

def atualizar_interface(msg):
    global log_box
    if log_box:
        log_box.markdown("```text\n{}\n```".format(msg))

def main():
    st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões - Deriv.com")

    st.markdown("Escolha a estratégia e configure os parâmetros abaixo.")

    token = st.text_input("🎯 Token da Deriv", type="password")
    estrategia = st.selectbox("📌 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    botao_iniciar = st.button("🚀 Iniciar Robô")

    global log_box
    log_box = st.empty()

    if botao_iniciar and token:
        atualizar_interface("🔌 Iniciando conexão com a Deriv...")
        iniciar_conexao(token, estrategia, atualizar_interface)
