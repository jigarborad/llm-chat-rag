import streamlit as st
from data_manager import DataManager
from open_ai_models import OpenAIModel
from groq_models import GroqModel
import openai
import time
class ChatApp:
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self.vector_store = None

    def response_generator(self, response):
        for word in response.split():
            yield word + " "
            time.sleep(0.05)

    def load_model(self):
        if self.model_name in OpenAIModel(self.api_key).get_available_models():
            self.model = OpenAIModel(self.api_key)
            self.vector_store = self.model.open_ai_embedding(self.vector_store_path, self.chunks)
        elif self.model_name in GroqModel(self.api_key).get_available_models():
            self.model = GroqModel(self.api_key)
            self.vector_store = self.model.local_embedding(self.vector_store_path, self.chunks)
        else:
            st.error("Selected model is not available.")
            return False
        return True
    
    def run(self):
        vector_store_path, chunks, uploaded_file = DataManager.pdf_uploader()
        if uploaded_file is not None:
            self.vector_store_path = vector_store_path
            self.chunks = chunks
            if not self.load_model():
                return

            st.success(f'PDF "{uploaded_file.name}" uploaded and processed successfully!')

            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Accept user input
            if prompt := st.chat_input("What is up?"):
                try:
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    # Display user message in chat message container
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Display assistant response in chat message container
                    response = self.model.query_model(self.model_name, prompt, self.vector_store)
                    with st.chat_message("assistant"):
                        st.write_stream(self.response_generator(response))
                    
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except openai.OpenAIError as e:
                    st.error(f"Error: {str(e)}. Please check your API key and try again.")
                    st.session_state.openai_api_key = ''
                    st.session_state.api_key_invalid = True
                    st.rerun()
