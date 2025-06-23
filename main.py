import streamlit as st
from deriv_ws import iniciar_conexao

def main():
    st.set_page_config(page_title="Robô Predador de Padrões", layout="centered")
    st.title("🤖 Robô Predador de Padrões")
    token = st.text_input("🔑 Insira seu Token da Deriv", type="password")
    estrategia = st.selectbox("🎯 Escolha a Estratégia", ["Predador de Padrões", "Identificador de Padrão"])
    stake = st.number_input("💵 Stake Inicial", min_value=0.35, value=1.0)
    martingale = st.checkbox("🎲 Ativar Martingale", value=True)
    fator_martingale = st.number_input("📈 Fator Martingale", min_value=1.0, value=2.0)
    botao = st.button("🚀 Iniciar Robô")
    placeholder_log = st.empty()

    if botao and token:
        placeholder_log.markdown("```text
🔌 Iniciando conexão com a Deriv...
```")
        iniciar_conexao(token, estrategia, stake, martingale, fator_martingale, placeholder_log)