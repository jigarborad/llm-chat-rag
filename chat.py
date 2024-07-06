import streamlit as st
import speech_recognition as sr
from open_ai_models import OpenAIModel
from groq_models import GroqModel
from utils import icon_loader
import chime

class ChatApp:
    def __init__(self, api_key, model_name, vector_store_path, chunks, uploaded_file):
        self.api_key = api_key
        self.model_name = model_name
        self.vector_store_path = vector_store_path
        self.chunks = chunks
        self.uploaded_file = uploaded_file
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

    def record_audio(self, recognizer, microphone):
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")
        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")

        # Adjust the recognizer sensitivity to ambient noise and record audio
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            chime.theme("material")
            st.toast('Listening ...')
            chime.info()
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            chime.info()
            st.toast('Listening Completed...')
        return audio
    def transcribe_speech(self, audio):
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
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API unavailable"
        except sr.UnknownValueError:
            response["error"] = "Unable to recognize speech"
        return response

    def run(self):
            if "messages" not in st.session_state:
                st.session_state.messages = []
            if self.uploaded_file is not None:
                if not self.load_model():
                    return
                
                default_instructions = (
                    "You are a PDF chat bot. Answer questions by reading the provided PDF documents with the context and source."
                    "If someone greets you, then answer it."
                    "If a question is outside the scope of these documents, respond with 'This question is not related to the document."
                    "Please ask questions related to the PDF."
                )

                # Initialize microphone state if not already present
                if "mic_active" not in st.session_state:
                    st.session_state.mic_active = False
                
                chat_input_container = st.container()
                
                
                with chat_input_container:
                    cols1 = st.columns([0.85, 0.1, 0.11, 0.1])
                    user_query = None
                    audio = None
                    if user_query2 := cols1[0].chat_input(placeholder="What's Up"):
                        user_query = user_query2
                    with cols1[1]:
                        if self.model_name in OpenAIModel(self.api_key).get_available_models():
                            disabled = True
                        else:
                            disabled = False
                        if st.button(":studio_microphone:", help="Mic (only available for Groq models)", disabled=disabled, use_container_width=True):
                            st.session_state.mic_active = not st.session_state.mic_active
                        if st.session_state.mic_active:
                            recognizer = sr.Recognizer()
                            microphone = sr.Microphone()
                            audio = self.record_audio(recognizer, microphone)
                            st.session_state.mic_active = False
                        if audio:
                            speech_response = self.transcribe_speech(audio)
                            if speech_response["success"]:
                                user_query = speech_response["transcription"]
                                
                    with cols1[2]:
                        with st.popover(label= ":pencil2:",help="Custom Instructions (Prompts)",use_container_width=True):
                            # User input for custom prompt template
                            custom_template = st.text_area("Enter your custom instructions", placeholder="default_instructions are\n\n" + default_instructions, height=100)

                        # Check if current custom template is different from the stored one
                        if "custom_template" in st.session_state and st.session_state.custom_template != custom_template:
                            st.session_state.custom_template = custom_template
                            st.session_state.messages = []  # Clear chat history

                        # If no custom template stored yet, store the current one
                        if "custom_template" not in st.session_state:
                            st.session_state.custom_template = custom_template or default_instructions
                    with cols1[3]:
                        if st.button(":broom:", help="Clear chat history",use_container_width=True):
                            st.session_state.messages = []
                    # Float button container
                chat_input_container.float('bottom: 1%; background-color:white; display: flex; justify-content: center; margin: 0 auto; padding: 10px; border-radius: 10px; border: 1; box-shadow: rgba(0, 0, 0, 0.35) 0px 5px 15px;')
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
                    with st.spinner("Thinking..."):
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
                    chime.warning()
                        # JavaScript to scroll to the bottom of the chat container
                
                
                js = f"""
                <script>
                    function scroll(dummy_var_to_force_repeat_execution) {{
                        var textAreas = parent.document.querySelectorAll('section.main');
                        for (let index = 0; index < textAreas.length; index++) {{
                            textAreas[index].scrollTop = textAreas[index].scrollHeight;
                        }}
                    }}
                    scroll({len(st.session_state.messages)})
                </script>
                """
                st.components.v1.html(js, height=0)
                    