import streamlit as st
import google.generativeai as genai

# Setup page
st.set_page_config(page_title="ChestyAI", page_icon="🦅")
st.title("🦅 ChestyAI")

# 1. Connect to Google
try:
    # Use the secret name you already set up
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Secret Error: {e}")
    st.stop()

# 2. Pick the most compatible model
# 'gemini-pro' is the industry standard that works everywhere
model = genai.GenerativeModel('gemini-pro')

# 3. The Chat Box
prompt = st.chat_input("Ask Chesty...")

if prompt:
    st.write(f"**You:** {prompt}")
    try:
        # Generate the response
        response = model.generate_content(prompt)
        st.write(f"**Chesty:** {response.text}")
    except Exception as e:
        st.error(f"AI Error: {e}")
