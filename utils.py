import streamlit as st

def som_sucesso():
    # Exemplo: não funciona no Streamlit Cloud offline, mas placeholder
    try:
        st.audio("https://www.soundjay.com/buttons/sounds/button-10.mp3", autoplay=True)
    except:
        pass

def som_erro():
    try:
        st.audio("https://www.soundjay.com/button/beep-07.wav", autoplay=True)
    except:
        pass