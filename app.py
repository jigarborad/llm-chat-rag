import streamlit as st
from css import styles
from css.sidebar import render_sidebar
from chat import chat

def main():
    # Set page config
    st.set_page_config(page_title="LLM Chat App", page_icon=":robot_face:", layout="centered")

    # Custom CSS for complete redesign
    st.markdown(styles.custom_css, unsafe_allow_html=True)

    # Sidebar contents
    option, api_key = render_sidebar()

    st.markdown(styles.header, unsafe_allow_html=True)
    chat(api_key, option)

if __name__ == "__main__":
    main()
