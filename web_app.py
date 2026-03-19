import streamlit as st
from google import genai
from google.genai import types

# Set up the web page title
st.title("🦅 ChestyAI")
st.subheader("USMC Professional Assistant")

# Paste your working API Key here!
API_KEY = st.secrets["GEMINI_API_KEY"]
# 1. Initialize the AI
client = genai.Client(api_key=API_KEY)

# 2. Set up the "memory" so the website remembers the conversation
if "chat" not in st.session_state:
    usmc_instructions = """
    You are ChestyAI, a professional, highly accurate, and respectful assistant built specifically for United States Marines. 
    Your expertise includes USMC History, MOS manuals, general orders, and leadership traits.
    Respond directly and with a professional military bearing.
    """
    config = types.GenerateContentConfig(system_instruction=usmc_instructions)
    # Start the chat
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash", config=config)
    st.session_state.messages = []

# 3. Draw all previous messages on the screen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Create the chat input box at the bottom of the screen
user_input = st.chat_input("Ask your USMC question, Marine...")

if user_input:
    # Display what the user typed
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Send to ChestyAI and display the response
    try:
        response = st.session_state.chat.send_message(user_input)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
