import streamlit as st
from deriv_ws import iniciar_conexao
import queue

log_queue = queue.Queue()

def atualizar_interface(mensagem):
    log_placeholder.markdown(f"```text\n{mensagem}\n```")

def main():
    st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")
    token = st.text_input("🔑 Token da Deriv", type="password")
    estrategia = st.selectbox("🎯 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    stake = st.number_input("💰 Stake inicial", min_value=0.35, value=1.00)
    martingale = st.checkbox("📈 Ativar Martingale", value=True)

    global log_placeholder
    log_placeholder = st.empty()

    if st.button("🚀 Iniciar robô"):
        st.success("Robô iniciado! Veja logs abaixo.")
        iniciar_conexao(token, stake, estrategia, martingale, log_queue)

    # Atualiza logs recebidos pela fila
    with st.container():
        log_text = ""
        while not log_queue.empty():
            log_text += log_queue.get() + "\n"
        log_placeholder.markdown(f"```text\n{log_text}\n```")