import streamlit as st
from google import genai
from google.genai import types

# Page Setup
st.set_page_config(page_title="ChestyAI", page_icon="🦅")
st.title("🦅 ChestyAI")
st.subheader("USMC Professional Assistant")

# 1. Securely get the API Key from your Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# 2. Initialize the AI and Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "chat" not in st.session_state:
    client = genai.Client(api_key=API_KEY)
    usmc_instructions = """
    You are ChestyAI, a professional and highly accurate assistant for US Marines. 
    You specialize in USMC History, Regulations (MCO), and Drill. 
    Maintain a professional military bearing at all times.
    """
    config = types.GenerateContentConfig(system_instruction=usmc_instructions)
    # Start the persistent chat session
    st.session_state.chat = client.chats.create(model="gemini-1.5-flash", config=config)

# 3. Display Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. User Input
user_input = st.chat_input("Ask your USMC question, Marine...")

if user_input:
    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get AI response using the persistent session
    try:
        response = st.session_state.chat.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
