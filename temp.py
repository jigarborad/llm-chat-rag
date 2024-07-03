import streamlit as st
import speech_recognition as sr
from data_manager import DataManager
from open_ai_models import OpenAIModel
from groq_models import GroqModel
from utils import icon_loader
from streamlit_float import *
# Float feature initialization
float_init()

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

    def recognize_speech_from_mic(self, recognizer, microphone):
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")
        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # Adjust the recognizer sensitivity to ambient noise and record audio
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        
        try:
            # Send audio data to Groq for transcription
            self.model = GroqModel(self.api_key)
            transcription = self.model.transcription_model(audio)

            response["transcription"] = transcription.text
            print(response, "groq transcription")
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"
        return response

    def run(self):
        
        vector_store_path, chunks, uploaded_file = DataManager.pdf_uploader()
        # Initialize chat history
        cc= st.container(height=400, border=False)
        with cc:
            if "messages" not in st.session_state:
                st.session_state.messages = []
            if uploaded_file is not None:
                self.vector_store_path = vector_store_path
                self.chunks = chunks
                if not self.load_model():
                    return
                
                default_instructions = (
                    "You are a PDF chat bot. Answer questions by reading the provided PDF documents with the context and source."
                    "If someone greets you, then answer it."
                    "If a question is outside the scope of these documents, respond with 'This question is not related to the document."
                    "Please ask questions related to the PDF."
                )

                

                # Display chat messages from history on app rerun
                chat_history_container = st.container()
                with chat_history_container:
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
                # Initialize microphone state if not already present
                if "mic_active" not in st.session_state:
                    st.session_state.mic_active = False

                chat_input_container = st.container()
                with chat_input_container:
                    cols1 = st.columns([0.82, 0.08, 0.11])
                    user_query = None
                    if user_query2 := cols1[0].chat_input(placeholder="What's Up"):
                        user_query = user_query2
                    with cols1[1]:
                        if st.button(":studio_microphone:", help="Click to activate microphone"):
                            st.session_state.mic_active = not st.session_state.mic_active
                        if st.session_state.mic_active:
                            recognizer = sr.Recognizer()
                            microphone = sr.Microphone()

                            speech_response = self.recognize_speech_from_mic(recognizer, microphone)
                            if speech_response["success"]:
                                user_query = speech_response["transcription"]
                                st.session_state.mic_active = False
                    with cols1[2]:
                        with st.popover(label= ":pencil2:",help="Custom Instructions"):
                            # User input for custom prompt template
                            custom_template = st.text_area("Enter your custom instructions", placeholder="default_instructions are\n\n" + default_instructions, height=100)

                        # Check if current custom template is different from the stored one
                        if "custom_template" in st.session_state and st.session_state.custom_template != custom_template:
                            st.session_state.custom_template = custom_template
                            st.session_state.messages = []  # Clear chat history

                        # If no custom template stored yet, store the current one
                        if "custom_template" not in st.session_state:
                            st.session_state.custom_template = custom_template or default_instructions
                    # Float button container
                chat_input_container.float('bottom: 5px; background-color:white; display: flex; justify-content: center; margin: 0 auto; padding: 10px; border-radius: 10px; border: 1; box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;')
                    
                if user_query:
                    # Add user message to chat history
                    st.session_state.messages.append({"role": "user", "content": user_query})
                    # Display user message in chat message container
                    st.markdown(
                        f'<div class="user-message-container">'
                        f'<div class="user-message">{user_query}</div>'
                        f'{icon_loader("images/profile.png")}</div>',
                        unsafe_allow_html=True
                    )

                    # Query model including the conversation history
                    history = [{"role": "user", "content": msg["content"]} if msg["role"] == "user" else {"role": "assistant", "content": msg["content"]} for msg in st.session_state.messages]
                    template = (st.session_state.custom_template or default_instructions) + "\n\n" + "{history}\n\nuser: {query}"
                    response = self.model.query_model(self.model_name, user_query, self.vector_store, history, template)

                    # Add assistant's response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    # Display assistant's message in chat message container
                    st.markdown(
                        f'<div class="assistant-message-container">'
                        f'{icon_loader("images/bot.png")}'
                        f'<div class="assistant-message">{response}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )