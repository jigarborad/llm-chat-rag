import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import utils

def render_sidebar():
    with st.sidebar:
        st.title("LLM Chat App")
        st.markdown('''
                    Welcome to the LLM Chat App! Please enter your name and start chatting.
                    ## About the app
                    The app is powered by:
                    - Streamlit
                    - LangChain
                    - OpenAI
                    ''')
        add_vertical_space(5)

        # Model selection
        with st.expander("Model Selection and API Key Input",  expanded=True):
            option = st.selectbox(
                label="Which model do you want to use?",
                options=("gpt_3_5_turbo_openai", None),
                placeholder="Select model...",
            )

            # API key input
            if option:    
                utils.get_openai_key()
                if not st.session_state.openai_api_key:
                    st.warning("Please enter your OpenAI API Key")
                else:
                    st.write("API Key entered successfully!")

        return option, st.session_state.openai_api_key
