import streamlit as st
import threading
from deriv_ws import iniciar_conexao

log_box = st.empty()

def atualizar_interface(msg):
    if 'log_text' not in st.session_state:
        st.session_state['log_text'] = ""
    st.session_state['log_text'] += f"{msg}\n"
    log_box.text_area("📜 LOG DE EVENTOS", value=st.session_state['log_text'], height=300)

def main():
    st.set_page_config(page_title="Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    token = st.text_input("🎯 Token da API Deriv")
    stake = st.number_input("💰 Stake inicial", min_value=0.35, value=1.00, step=0.01)
    usar_martingale = st.checkbox("📈 Ativar Martingale", value=True)
    estrategia = st.selectbox("🎯 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])

    if st.button("🚀 Iniciar Robô"):
        if token:
            threading.Thread(
                target=iniciar_conexao,
                args=(token, stake, usar_martingale, estrategia, atualizar_interface),
                daemon=True
            ).start()
            atualizar_interface("🔌 Iniciando conexão com a Deriv...")
        else:
            st.warning("⚠️ Insira um token válido.")