import streamlit as st
from agent import process_message

st.set_page_config(page_title="RTO Sahayak", layout="wide")

st.warning("Synthetic data demo. No real government systems.")
st.title("RTO Sahayak")

if "history" not in st.session_state:
    st.session_state.history = []
    
if "tool_calls" not in st.session_state:
    st.session_state.tool_calls = []

# Sidebar
st.sidebar.title("Latest Tool Calls")
if st.session_state.tool_calls:
    for tc in st.session_state.tool_calls:
        st.sidebar.write(tc)
else:
    st.sidebar.write("No tool calls yet.")

# Chat history
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["text"])

# Input
if prompt := st.chat_input("How can I help you?"):
    with st.chat_message("user"):
        st.write(prompt)
    
    # Process
    with st.spinner("Thinking..."):
        result = process_message(prompt, st.session_state.history)
        
        st.session_state.history.append({"role": "user", "text": prompt})
        st.session_state.history.append({"role": "model", "text": result["answer"]})
        st.session_state.tool_calls = result["tool_calls"]
        
        st.rerun()
