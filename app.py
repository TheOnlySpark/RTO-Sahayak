import streamlit as st
from agent import process_message
import uuid

st.set_page_config(page_title="RTO Sahayak", layout="wide")

st.warning("Synthetic data demo. No real government systems.")
st.title("RTO Sahayak")

if "history" not in st.session_state:
    st.session_state.history = []
    
if "tool_calls" not in st.session_state:
    st.session_state.tool_calls = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = {}

# Sidebar
st.sidebar.title("Latest Tool Calls")
if st.session_state.tool_calls:
    for tc in st.session_state.tool_calls:
        st.sidebar.write(tc)
else:
    st.sidebar.write("No tool calls yet.")

st.sidebar.markdown("---")
st.sidebar.write("Upload only synthetic sample documents.")
uploaded_file = st.sidebar.file_uploader("Upload Document", type=["jpg", "png", "jpeg"])
if uploaded_file is not None:
    # Use the filename as a predictable ID or just create one. 
    # To make it easier for the model, we can just use the filename as ID.
    file_id = uploaded_file.name
    st.session_state.uploaded_files[file_id] = uploaded_file.getvalue()
    st.sidebar.success(f"File uploaded! ID: {file_id}")
    st.sidebar.info("You can refer to this file by its ID.")

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
