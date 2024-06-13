import streamlit as st

def validate_openai_key(api_key):
    """Check if the API key starts with 'sk-'."""
    return api_key.startswith("sk-")

def get_openai_key():
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ''
        st.session_state.api_key_invalid = False  # Track if API key is invalid

    # Generate a unique key for the text input widget
    input_key = "openai_api_key_input"
    api_key_input = None
    # Display input field for API key with a unique key
    if not st.session_state.openai_api_key:
        api_key_input = st.text_input(
            label="Enter your OpenAI API Key",
            key=input_key,
            type="password"
        ).strip()

    if api_key_input:
        if validate_openai_key(api_key_input):
            st.session_state.openai_api_key = api_key_input
            st.session_state.api_key_invalid = False  # Reset invalid flag
        else:
            st.session_state.api_key_invalid = True
            st.error("Invalid API key. Please enter a valid OpenAI API key starting with 'sk-'.")
            st.session_state.openai_api_key = ''  # Clear the key

    return st.session_state.openai_api_key
