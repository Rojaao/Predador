import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Predador de Padrões - por Rogger", layout="centered")
    st.title("🤖 Predador de Padrões - por Rogger")

    token = st.text_input("🔑 Token Deriv (Real ou Demo)")
    stake = st.number_input("💵 Stake Inicial", min_value=0.35, value=1.00)
    martingale = st.checkbox("🔁 Ativar Martingale", value=True)
    fator = st.number_input("📈 Fator Martingale", value=2.0)
    stop_loss = st.number_input("🛑 Stop Loss", value=20.0)
    stop_gain = st.number_input("🎯 Stop Gain", value=50.0)

    status_box = st.empty()
    log_box = st.empty()

    def atualizar_interface(msg):
        historico = log_box.text_area("📜 LOG DE EVENTOS", value=msg, height=300)
        status_box.success("✅ Robô Rodando...")

    if st.button("🚀 Iniciar Robô"):
        status_box.info("⏳ Iniciando conexão com Deriv...")
        iniciar_conexao(token, stake, martingale, fator, stop_loss, stop_gain, atualizar_interface)

if __name__ == "__main__":
    main()