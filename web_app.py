import streamlit as st
from google import genai

st.set_page_config(page_title="ChestyAI", page_icon="🦅")
st.title("🦅 ChestyAI")
st.subheader("USMC Assistant")

# 1. Get Key
API_KEY = st.secrets["GEMINI_API_KEY"]

# 2. Setup Client
client = genai.Client(api_key=API_KEY)

# 3. Simple Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 4. Input
prompt = st.chat_input("Ask Chesty...")

if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate Response
    try:
        # We use 'generate_content' instead of 'chats.create' to avoid the "closed" error
        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=prompt,
            config={'system_instruction': 'You are ChestyAI, a USMC assistant.'}
        )
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"Error: {e}")
