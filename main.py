import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")

    with st.sidebar:
        st.header("⚙️ Configurações")
        token = st.text_input("🎯 Token da Deriv", type="password")
        stake_inicial = st.number_input("💵 Stake Inicial", value=1.0)
        martingale = st.checkbox("📈 Ativar Martingale", value=True)
        fator_martingale = st.number_input("✖️ Fator Martingale", value=2.0)
        stop_loss = st.number_input("❌ Stop Loss", value=10.0)
        stop_gain = st.number_input("✅ Meta de Lucro", value=10.0)
        iniciar = st.button("🚀 Iniciar Robô")

    status_box = st.empty()
    log_box = st.empty()
    historico_box = st.empty()

    if iniciar and token:
        status_box.success("Robô iniciado!")
        historico = []
        def atualizar_interface(info):
            if 'log' in info:
                log_box.code(info['log'], language='text')
            if 'status' in info:
                status_box.info(info['status'])
            if 'historico' in info:
                historico_box.table(info['historico'])

        iniciar_conexao(
            token=token,
            stake=stake_inicial,
            martingale=martingale,
            fator_martingale=fator_martingale,
            stop_loss=stop_loss,
            stop_gain=stop_gain,
            atualizar_interface=atualizar_interface
        )