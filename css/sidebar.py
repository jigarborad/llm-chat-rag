import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space

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
        st.write("Made with ❤️ by [Jigar](https://github.com/jigarborad)")
