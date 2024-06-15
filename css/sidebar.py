import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import utils
from open_ai_models import OpenAIModel
from groq_models import GroqModel

def render_sidebar():
    with st.sidebar:
        st.title("LLM Chat App")
        st.markdown('''Welcome to the LLM Chat App! Please enter your name and start chatting.''')
        add_vertical_space(1)
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
                    label="Which model do you want to use?",
                    options=groq_model.get_available_models(),
                    placeholder="Select model...",
                )
        add_vertical_space(1)
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
        add_vertical_space(1)
        st.write("Made with ❤️ by [Jigar](https://github.com/jigarborad)")

        
        return model, api_key
