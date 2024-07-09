import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import utils
from open_ai_models import OpenAIModel
from groq_models import GroqModel
from data_manager import DataManager
def render_sidebar():
    with st.sidebar:
        st.title("PDF Chat App")
        st.markdown('''Welcome to the LLM Chat App! Please enter your name and start chatting.''')
        # Model selection
        with st.expander("Model Selection and API Key Input", expanded=True):
            service = st.selectbox(
                label="Which service do you want to use?",
                options=("OpenAI", "Groq"),
                placeholder="Select service..."
            )

            model = None
            api_key = None
            if service == "OpenAI":
                api_key = utils.get_openai_key()
                openai_model = OpenAIModel(api_key)
                model = st.selectbox(
                    label="Which model do you want to use?",
                    options=openai_model.get_available_models(),
                    placeholder="Select model...",
                )
            elif service == "Groq":
                api_key = utils.get_groq_key()
                groq_model = GroqModel(api_key)
                model = st.selectbox(
                    label="Which model do you want to use?a",
                    options=groq_model.get_available_models(),
                    placeholder="Select model...",
                )
          # Check if API key is entered before calling pdf_uploader
            vector_store_path, chunks, uploaded_file = None, None, None
            if api_key:
                vector_store_path, chunks, uploaded_file = DataManager.pdf_uploader()
        st.markdown('''
                    ## About the app
                    The app is powered by:
                    - Streamlit
                    - LangChain
                    - OpenAI
                    - Groq
                    - FAISS
                    - Huggingface
                    ''')
        st.write("Made with ❤️ by [Jigar](https://github.com/jigarborad)")

        
        return model, api_key,vector_store_path, chunks, uploaded_file
