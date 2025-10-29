# client.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8080/ask"  # FastAPI endpoint

st.title("NEET Helper")
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for role, text in st.session_state.messages:
    st.chat_message(role).write(text)

if query := st.chat_input("What do you need help with?"):
    st.session_state.messages.append(("user", query))
    st.chat_message("user").write(query)

    # Send query to FastAPI backend
    with st.spinner("Thinking..."):
        response = requests.post(API_URL, json={"query": query})
        if response.status_code == 200:
            answer = response.json().get("answer")
        else:
            answer = "Error: Unable to fetch response from server."

    st.session_state.messages.append(("assistant", answer))
    st.chat_message("assistant").write(answer)
    st.badge("Success", icon=":material/check:", color="green")
