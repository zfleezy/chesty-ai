import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(page_title="ChestyAI", page_icon="🦅")
st.title("🦅 ChestyAI")
st.subheader("USMC Assistant")

# 2. Key Check
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Missing API Key! Add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 3. Setup Client
client = genai.Client(api_key=API_KEY)

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
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are ChestyAI, a legendary USMC assistant. Respond with professional military bearing and accuracy."
            )
        )
        
        # Display Chesty's answer
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Signal Lost: {e}")
