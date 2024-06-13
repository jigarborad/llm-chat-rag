import streamlit as st

def get_openai_key():
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ''
        st.session_state.api_key_invalid = False  # Track if API key is invalid

    if not st.session_state.openai_api_key:
        if st.session_state.api_key_invalid:
            st.error("Invalid API key. Please enter a valid OpenAI API key.")
        st.session_state.openai_api_key = st.text_input(
            "Enter your OpenAI API Key", type="password"
        )