import streamlit as st
import openai
from data_manager import DataManager
from open_ai_models import OpenAIModel
from groq_models import GroqModel
from utils import icon_loader

class ChatApp:
    def __init__(self, api_key, model_name):
        self.api_key = api_key
        self.model_name = model_name
        self.model = None
        self.vector_store = None

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
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if uploaded_file is not None:
            self.vector_store_path = vector_store_path
            self.chunks = chunks
            
            if not self.load_model():
                return
            st.success(f'PDF "{uploaded_file.name}" uploaded and processed successfully!')
            default_instructions = (
                    "You are a PDF chat bot. Answer questions by reading the provided PDF documents with the context and source."
                    "if you greets you, then answer it"
                    "If a question is outside the scope of these documents, respond with 'This question is not related to the document."
                    "Please ask questions related to the PDF.")
            
            with st.popover("Custom Instructions"):
                # User input for custom prompt template
                custom_template = st.text_area("Enter your custom instructions", placeholder="default_instructions are\n\n" + default_instructions, height=100)
                
            # Check if current custom template is different from the stored one
            if "custom_template" in st.session_state and st.session_state.custom_template != custom_template:
                st.session_state.custom_template = custom_template
                st.session_state.messages = []  # Clear chat history
            
            # If no custom template stored yet, store the current one
            if "custom_template" not in st.session_state:
                st.session_state.custom_template = custom_template or default_instructions
            # Display chat messages from history on app rerun
            for message in st.session_state.messages:
                if message["role"] == "user":
                    st.markdown(
                        f'<div class="user-message-container">'
                        f'<div class="user-message">{message["content"]}</div>'
                        f'{icon_loader("images/profile.png")}</div>', 
                        unsafe_allow_html=True
                    )
                elif message["role"] == "assistant":
                    st.markdown(
                        f'<div class="assistant-message-container">'
                        f'{icon_loader("images/bot.png")}'
                        f'<div class="assistant-message">{message["content"]}</div>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )

            # Accept user input
            if prompt := st.chat_input("What is up?"):
                try:
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": prompt})
                    # Display user message in chat message container
                    st.markdown(
                        f'<div class="user-message-container">'
                        f'<div class="user-message">{prompt}</div>'
                        f'{icon_loader("images/profile.png")}</div>', 
                        unsafe_allow_html=True
                    )

                    # Query model including the conversation history
                    history = [{"role": "user", "content": msg["content"]} if msg["role"] == "user" else {"role": "assistant", "content": msg["content"]} for msg in st.session_state.messages]
                    template = (st.session_state.custom_template or default_instructions) + "\n\n"+"{history}\n\nuser: {query}"
                    

                    with st.spinner("Thinking... ... ..."):
                        response = self.model.query_model(self.model_name, prompt, self.vector_store, history, template)

                    # Add assistant's response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                    # Display assistant's response
                    st.markdown(
                        f'<div class="assistant-message-container">'
                        f'{icon_loader("images/bot.png")}'
                        f'<div class="assistant-message">{response}</div>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )

                except openai.OpenAIError as e:
                    st.error(f"Error: {str(e)}. Please check your API key and try again.")
                    st.session_state.openai_api_key = ''
                    st.session_state.api_key_invalid = True
                    st.rerun()