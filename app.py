import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Techculture Assistant",
    page_icon="🤖",
    layout="centered"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0 0.5rem;
    }
    .main-header h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
    }
    .main-header p {
        color: #888;
        font-size: 1rem;
    }
    .stChatMessage {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown("""
<div class="main-header">
    <h1>🤖 Techculture Assistant</h1>
    <p>Ask me anything about our services, pricing, and more</p>
</div>
""", unsafe_allow_html=True)

# --- Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat Input ---
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": prompt},
                    timeout=60
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "No answer received.")
                else:
                    answer = f"Error: {response.status_code} - {response.text}"
            except requests.exceptions.ConnectionError:
                answer = "⚠️ Cannot connect to the API server. Make sure it's running with:\n\n`uvicorn api:app --reload --port 8000`"
            except Exception as e:
                answer = f"⚠️ Something went wrong: {str(e)}"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
