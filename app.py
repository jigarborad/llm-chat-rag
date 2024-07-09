import streamlit as st
from css import styles, sidebar
from chat import ChatApp
from streamlit_float import *
# Float feature initialization
float_init()
def main():
    # Set page config
    #st.set_page_config(page_title="PDF Chat App", page_icon=":robot_face:", layout="centered")

    # Custom CSS for complete redesign
    st.markdown(styles.custom_css, unsafe_allow_html=True)

    # Sidebar contents
    model_name, api_key, vector_store_path, chunks, uploaded_file = sidebar.render_sidebar()
    blank_header = st.container()
    with blank_header:
        st.markdown(styles.blank_header, unsafe_allow_html=True)
    blank_header.float('top:0;')
    header_container = st.container()
    with header_container:
        st.markdown(styles.header, unsafe_allow_html=True)
    header_container.float('top: 5%;background-color:white; display: flex; justify-content: center; margin: 0 auto; padding: 10px; border-radius: 10px; border: 1; box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;')
    # Run chat app
    blank_footer = st.container()
    with blank_footer:
        st.markdown(styles.blank_footer, unsafe_allow_html=True)    
    
    blank_footer.float('bottom:0;')
    if api_key and model_name:
        chat_app = ChatApp(api_key, model_name, vector_store_path, chunks, uploaded_file)
        chat_app.run()

if __name__ == "__main__":
    main()
