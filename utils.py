import streamlit as st

def som_sucesso():
    st.audio("https://www.soundjay.com/buttons/sounds/button-10.mp3", autoplay=True)

def som_erro():
    st.audio("https://www.soundjay.com/button/beep-07.wav", autoplay=True)