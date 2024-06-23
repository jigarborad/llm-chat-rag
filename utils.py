import streamlit as st
import base64
from pathlib import Path

def get_openai_key():
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ''
        st.session_state.api_key_invalid = False

    input_key = "openai_api_key_input"
    api_key_input = None

    if not st.session_state.openai_api_key:
        api_key_input = st.text_input(
            label="Enter your OpenAI API Key",
            key=input_key,
            type="password"
        ).strip()

    if api_key_input:
        if api_key_input.startswith("sk-"):
            st.session_state.openai_api_key = api_key_input
            st.session_state.api_key_invalid = False
        else:
            st.session_state.api_key_invalid = True
            st.error("Invalid API key. Please enter a valid OpenAI API key starting with 'sk-'.")
            st.session_state.openai_api_key = ''
    st.markdown("[Create OpenAI API Key here](https://platform.openai.com/settings/profile?tab=api-keys)")
    return st.session_state.openai_api_key

def get_groq_key():
    if 'groq_api_key' not in st.session_state:
        st.session_state.groq_api_key = ''
        st.session_state.api_key_invalid = False

    input_key = "groq_api_key_input"
    api_key_input = None

    if not st.session_state.groq_api_key:
        api_key_input = st.text_input(
            label="Enter your Groq API Key",
            key=input_key,
            type="password"
        ).strip()

    if api_key_input:
        if api_key_input.startswith("gsk_"):  # Add your Groq API key validation logic here
            st.session_state.groq_api_key = api_key_input
            st.session_state.api_key_invalid = False
        else:
            st.session_state.api_key_invalid = True
            st.error("Invalid API key. Please enter a valid Groq API key.")
            st.session_state.groq_api_key = ''
    st.markdown("[Create Groq API Key here](https://console.groq.com/keys)")
    return st.session_state.groq_api_key

def icon_loader(img_path):
        img_bytes = Path(img_path).read_bytes()
        encoded = base64.b64encode(img_bytes).decode()
        img_html = "<img src='data:image/png;base64,{}' class='img-fluid icons-images'>".format(encoded)
        return img_html