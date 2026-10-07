"""Webová aplikácia: rozhovor s AI agentom v prehliadači."""

import streamlit as st
from google import genai

from agent import vytvor_chat

st.title("AI asistent poisťovne")
st.caption("Ukážkový projekt. Všetky dáta sú vymyslené.")

# Streamlit spúšťa tento súbor pri každom kliknutí odznova,
# preto si rozhovor pamätáme v st.session_state
if "chat" not in st.session_state:
    st.session_state.klient = genai.Client()  # kľúč si načíta z GEMINI_API_KEY
    st.session_state.chat = vytvor_chat(st.session_state.klient)
    st.session_state.spravy = []

for rola, text in st.session_state.spravy:
    st.chat_message(rola).write(text)

otazka = st.chat_input("Napríklad: Ktorý kraj minul najviac na lieky?")

if otazka:
    st.chat_message("user").write(otazka)

    try:
        with st.spinner("Premýšľam..."):
            odpoved = st.session_state.chat.send_message(otazka).text

    except Exception as chyba:
        st.error(f"AI teraz neodpovedá: {chyba}")
        st.stop()

    odpoved = odpoved or "Prepáč, na toto neviem odpovedať."

    st.chat_message("assistant").write(odpoved)

    st.session_state.spravy.append(("user", otazka))
    st.session_state.spravy.append(("assistant", odpoved))