import streamlit as st
from css import styles, sidebar
import utils
import data_manager
from open_ai_models import open_ai_embedding,  gpt_turbo_3_5

# Set page config
st.set_page_config(page_title="LLM Chat App", page_icon=":robot_face:", layout="centered")

# Custom CSS for complete redesign
st.markdown(styles.custom_css, unsafe_allow_html=True)

# Sidebar contents
sidebar.render_sidebar()


def chat_with_llm():
    option = st.selectbox(
        "Which model you wants to use?",
        ("gpt_3_5_turbo_openai","None"),
        index=None,
        placeholder="Select model...",)
    if option == "gpt_3_5_turbo_openai":
        utils.get_openai_key()
        vector_store_path, chunks, uploaded_file = data_manager.pdf_uploader()
        if uploaded_file is not None:
            VectorStore = open_ai_embedding(vector_store_path, chunks)
            st.success(f'PDF "{uploaded_file.name}" uploaded and processed successfully!')

            # Input for the query
            query = st.text_input("Shoot your question related to the PDF")

            if query:
                response = gpt_turbo_3_5(query, VectorStore)
                st.markdown(f'<div class="fade-in">{response}</div>', unsafe_allow_html=True)

def main():
    st.markdown(styles.header, unsafe_allow_html=True)

    st.markdown(styles.upload_banner, unsafe_allow_html=True)
    chat_with_llm()
    

if __name__ == "__main__":
    main()
