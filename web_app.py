import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="ChestyAI", page_icon="🦅")
st.title("🦅 ChestyAI")
st.subheader("USMC Assistant")

# 2. Key Check & Configuration
try:
    # Pulls from your Streamlit Secrets "GEMINI_API_KEY"
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 3. Setup the AI Model (Directly using the stable name)
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="You are ChestyAI, a legendary USMC assistant. Respond with professional military bearing and precision."
    )

# 4. Initialize History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. User Input
prompt = st.chat_input("Ask Chesty...")

if prompt:
    # Display user's question
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get Response from Google
    try:
        response = st.session_state.model.generate_content(prompt)
        
        # Display Chesty's answer
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Signal Lost: {e}")
