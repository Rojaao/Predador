import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Predador de Padrões - Robô Deriv", layout="centered")
    st.title("🤖 Predador de Padrões")

    st.markdown("Insira seu token da Deriv e clique em **Iniciar Robô** para operar automaticamente com a estratégia baseada em comportamento.")

    token = st.text_input("🔑 Token da Deriv")
    stake = st.number_input("💵 Stake Inicial ($)", min_value=0.35, value=1.00)
    martingale = st.checkbox("Ativar Martingale?", value=True)
    fator = st.number_input("🔁 Fator Martingale", value=2.0)
    stop_loss = st.number_input("🔻 Stop Loss ($)", value=20.0)
    stop_gain = st.number_input("🔺 Stop Gain ($)", value=50.0)

    if st.button("🚀 Iniciar Robô"):
        st.success("Robô iniciado!")
        iniciar_conexao(token, stake, martingale, fator, stop_loss, stop_gain, atualizar_interface)

def atualizar_interface(mensagem):
    if 'log' in mensagem:
        st.info(mensagem['log'])

if __name__ == "__main__":
    main()
