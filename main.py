
import streamlit as st
from deriv_ws import iniciar_conexao

log_box = None

def atualizar_interface(msg):
    global log_box
    if log_box:
        log_box.markdown(f"```text\n{msg}\n```")

def iniciar_app():
    global log_box
    st.set_page_config(page_title="Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    token = st.text_input("🎯 Insira seu token da Deriv", type="password")
    if st.button("🚀 Iniciar Robô"):
        if token:
            log_box = st.empty()
            atualizar_interface("🔌 Iniciando conexão com a Deriv...")
            iniciar_conexao(token, atualizar_interface)
        else:
            st.warning("⚠️ Por favor, insira um token válido.")
