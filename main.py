
import streamlit as st
from deriv_ws import iniciar_conexao
from estrategias import predador_de_padroes, identificador_de_padrao

estrategias = {
    "Predador de Padrões": predador_de_padroes,
    "Identificador de Padrão": identificador_de_padrao
}

log_box = st.empty()

def atualizar_interface(msg):
    log_box.text_area("📜 LOG DE EVENTOS", value=msg, height=300)

def main():
    st.set_page_config(page_title="Robô Deriv: Estratégias de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")
    st.markdown("Conecte-se com seu token e escolha a estratégia para começar.")

    token = st.text_input("🎯 Token da Deriv", type="password")
    stake = st.number_input("💰 Stake Inicial", min_value=0.35, value=1.00)
    martingale = st.checkbox("📈 Ativar Martingale", value=True)
    fator_martingale = st.number_input("⚙️ Fator de Martingale", min_value=1.0, value=2.0)
    estrategia_escolhida = st.selectbox("🎯 Estratégia:", list(estrategias.keys()))
    botao = st.button("🚀 Iniciar Robô")

    if botao and token:
        atualizar_interface("🔌 Iniciando conexão com a Deriv...")
        funcao_estrategia = estrategias[estrategia_escolhida]
        iniciar_conexao(token, stake, martingale, fator_martingale, funcao_estrategia, atualizar_interface)
