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
    st.error("Missing API Key in Secrets!")
    st.stop()

# 3. Setup Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are ChestyAI, a legendary USMC assistant. Respond with professional military bearing."
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
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        # Using the older, standard 'generate_content' method
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"Signal Lost: {e}")
