import streamlit as st
from deriv_ws import iniciar_conexao
from estrategias import predador_de_padroes, nova_estrategia

log_box = None

def atualizar_interface(msg):
    global log_box
    if log_box:
        log_box.markdown("```text\n{}\n```".format(msg))

def main():
    st.set_page_config(page_title="Robô Predador", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    global log_box
    log_box = st.empty()

    token = st.text_input("🔑 Token da API da Deriv", type="password")
    stake = st.number_input("💵 Stake inicial", min_value=0.35, value=1.00, step=0.35)
    estrategia = st.selectbox("🎯 Estratégia", ["Predador de Padrões", "Nova Estratégia"])
    botao_iniciar = st.button("🚀 Iniciar Robô")

    if botao_iniciar and token:
        atualizar_interface("🔌 Iniciando conexão com a Deriv...")
        estrategia_func = predador_de_padroes if estrategia == "Predador de Padrões" else nova_estrategia
        iniciar_conexao(token, stake, estrategia_func, atualizar_interface)