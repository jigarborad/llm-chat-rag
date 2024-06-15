import streamlit as st
from css import styles, sidebar
from chat import ChatApp

def main():
    # Set page config
    st.set_page_config(page_title="LLM Chat App", page_icon=":robot_face:", layout="centered")

    # Custom CSS for complete redesign
    st.markdown(styles.custom_css, unsafe_allow_html=True)

    # Sidebar contents
    model_name, api_key = sidebar.render_sidebar()

    st.markdown(styles.header, unsafe_allow_html=True)

    # Run chat app
    if api_key and model_name:
        chat_app = ChatApp(api_key, model_name)
        chat_app.run()

if __name__ == "__main__":
    main()
