import streamlit as st
import threading
from deriv_ws import iniciar_conexao

st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")
log_box = st.empty()

st.title("🤖 Robô Predador de Padrões")
token = st.text_input("🔑 Insira seu Token da Deriv", type="password")
martingale = st.checkbox("🎯 Ativar Martingale")
stake = st.number_input("💵 Stake Inicial", min_value=0.35, value=1.0, step=0.1)
estrategia = st.selectbox("📈 Estratégia", ["Predador de Padrões", "Identificador de Padrão"])

start = st.button("🚀 Iniciar Robô")

def atualizar_interface(msg):
    historico = log_box.text_area("📜 LOG DE EVENTOS", value=msg, height=300)

if start and token:
    threading.Thread(target=iniciar_conexao, args=(token, stake, martingale, estrategia, atualizar_interface)).start()
    atualizar_interface("🔌 Iniciando conexão com a Deriv...")
