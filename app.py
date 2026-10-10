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
        func_name = tc.get("name", "Unknown")
        args = tc.get("args", {})
        st.sidebar.markdown(f"**🛠️ {func_name}**")
        for key, val in args.items():
            st.sidebar.caption(f"↳ {key}: {val}")
else:
    st.sidebar.write("No tool calls yet.")

st.sidebar.markdown("---")
st.sidebar.write("Upload only synthetic sample documents.")
uploaded_files = st.sidebar.file_uploader("Upload Document(s)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
if uploaded_files:
    for f in uploaded_files:
        file_id = f.name
        st.session_state.uploaded_files[file_id] = f.getvalue()
        st.sidebar.success(f"File uploaded! ID: {file_id}")
    st.sidebar.info("You can refer to these files by their IDs.")

# Check if a PDF was generated
pdf_generated = False
for msg in reversed(st.session_state.history):
    if msg["role"] == "model" and any(tc.get("name") == "generate_handoff_pdf" for tc in st.session_state.tool_calls):
        pdf_generated = True
        break

if pdf_generated:
    st.success("Your PDF is ready!")
    st.download_button(
        label="📄 Download Handoff PDF",
        data=b"Mock PDF Content - DRAFT - for citizen review and officer verification - Replace with real bytes in production.",
        file_name="handoff.pdf",
        mime="application/pdf"
    )

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
        # Inject file context so the model knows what files are available
        file_ids = list(st.session_state.uploaded_files.keys())
        context = f"\n\n[System Context: Available uploaded file IDs: {file_ids}]" if file_ids else ""
        
        result = process_message(prompt + context, st.session_state.history)
        
        st.session_state.history.append({"role": "user", "text": prompt})
        st.session_state.history.append({"role": "model", "text": result["answer"]})
        st.session_state.tool_calls = result["tool_calls"]
        
        st.rerun()
