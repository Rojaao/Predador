import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Predador de Padrões - por Rogger", layout="centered")
    st.title("🤖 Predador de Padrões - por Rogger")

    strategy = st.selectbox("Selecione a estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    token = st.text_input("🔑 Token Deriv (Real ou Demo)")
    stake = st.number_input("💵 Stake Inicial", min_value=0.35, value=1.00)
    martingale = st.checkbox("🔁 Ativar Martingale", value=True)
    fator = st.number_input("📈 Fator Martingale", value=2.0)
    stop_loss = st.number_input("🛑 Stop Loss", value=20.0)
    stop_gain = st.number_input("🎯 Stop Gain", value=50.0)

    status_box = st.empty()
    log_box = st.empty()

    if st.button("🚀 Iniciar Robô"):
        if not token:
            st.error("Insira token válido.")
        else:
            status_box.info("⏳ Iniciando conexão...")
            strat_key = 'predador' if strategy=="Predador de Padrões" else 'identificador'
            iniciar_conexao(token, stake, martingale, fator, stop_loss, stop_gain, strat_key, lambda msg: log_box.markdown(f"```text\n{msg}\n```"))

    if st.button("🔄 Atualizar Logs"):
        # Apenas rerun para exibir logs empilhados
        st.experimental_rerun()

if __name__ == "__main__":
    main()