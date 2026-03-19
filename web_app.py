import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="ChestyAI", page_icon="🦅")
st.title("🦅 ChestyAI")
st.subheader("USMC Assistant")

# 2. Key Check
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 3. Setup Model - Using the EXACT name requested by your server
if "chat" not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# Display previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. User Input
prompt = st.chat_input("Ask Chesty...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Standard chat response
        response = st.session_state.chat.send_message(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        # This will show the error if it still fails
        st.error(f"Error: {e}")
