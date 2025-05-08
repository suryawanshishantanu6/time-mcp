import streamlit as st
import requests

MCP_SERVER_URL = 'http://localhost:5002/chat'

st.set_page_config(page_title="AI Chat Agent", page_icon="🤖")
st.title("AI Chat Agent")

if 'history' not in st.session_state:
    st.session_state['history'] = []

user_input = st.text_input("You:", "", key="input")

if st.button("Send") and user_input.strip():
    resp = requests.post(MCP_SERVER_URL, json={"message": user_input})
    if resp.status_code == 200:
        ai_reply = resp.json().get('response', '')
    else:
        ai_reply = "[Error: No response from agent]"
    st.session_state['history'].append((user_input, ai_reply))
    st.rerun()

for user, ai in st.session_state['history']:
    st.markdown(f"**You:** {user}")
    st.markdown(f"**AI:** {ai}")
