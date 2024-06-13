import streamlit as st
import utils
import data_manager
from open_ai_models import open_ai_embedding, gpt_turbo_3_5
import openai
import time

def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


def chat():
    option = st.selectbox(
        label="Which model do you want to use?",
        options =("gpt_3_5_turbo_openai", "None"),
        index=None,
        placeholder="Select model...",
    )

    if option == "gpt_3_5_turbo_openai":
        utils.get_openai_key()

        if st.session_state.openai_api_key:
            # Proceed to PDF upload and interaction only if the API key is entered
            
            vector_store_path, chunks, uploaded_file = data_manager.pdf_uploader()
            if uploaded_file is not None:
                VectorStore = open_ai_embedding(vector_store_path, chunks, st.session_state.openai_api_key)
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
                    

                    if st.session_state.openai_api_key:
                        # Proceed to generate response only if the API key is entered
                        try:
                            
                            # Add user message to chat history
                            st.session_state.messages.append({"role": "user", "content": prompt})
                            # Display user message in chat message container
                            with st.chat_message("user"):
                                st.markdown(prompt)
                            # Display assistant response in chat message container
                            response = gpt_turbo_3_5(prompt, VectorStore, st.session_state.openai_api_key)
                            
                            with st.chat_message("assistant"):
                                response = st.write_stream(response_generator(response))
                                #st.markdown(response)
                            st.session_state.messages.append({"role": "assistant", "content": response})
                        except openai.OpenAIError as e:
                            st.error(f"Error: {str(e)}. Please check your API key and try again.")
                            st.session_state.openai_api_key = ''
                            st.session_state.api_key_invalid = True
                            st.rerun()