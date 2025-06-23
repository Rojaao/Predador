import streamlit as st
from bot_core import iniciar_robo

st.set_page_config(page_title="Predador de Padrões - por Rogger", layout="centered")
st.title("🧠 Predador de Padrões")

if "status" not in st.session_state:
    st.session_state.status = "⏹ Parado"

token = st.text_input("🔑 Insira seu token da Deriv (real ou demo)", type="password")
if st.button("▶ Iniciar Robô"):
    if token:
        st.session_state.status = "🚀 Rodando..."
        iniciar_robo(token)
    else:
        st.warning("Insira um token válido.")

st.subheader("📈 Status do Robô")
st.text(f"Status atual: {st.session_state.status}")

st.subheader("💰 Lucro Acumulado (USD)")
st.text("$0.00")