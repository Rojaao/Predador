
import streamlit as st
from deriv_ws import iniciar_conexao
from estrategias import predador_de_padroes, outra_estrategia

log_box = None

def atualizar_interface(msg):
    global log_box
    if log_box:
        log_box.markdown(f"```text\n{msg}\n```")

def main():
    global log_box
    st.set_page_config(page_title="Predador de Padrões", layout="centered")
    st.title("🤖 Predador de Padrões da Deriv")

    token = st.text_input("🔑 Token da Deriv", type="password")
    estrategia = st.selectbox("📈 Estratégia", ["Predador de Padrões", "Outra Estratégia"])

    log_box = st.empty()

    if st.button("▶️ Iniciar Robô"):
        atualizar_interface("🔌 Iniciando conexão com a Deriv...")
        iniciar_conexao(token, atualizar_interface, estrategia)
