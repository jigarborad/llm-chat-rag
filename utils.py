import os
import streamlit as st
from dotenv import load_dotenv

def get_openai_key():
    #load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    #if not openai_api_key:
    openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
    # if openai_api_key:
    #    with open('.env', 'a') as f:
    #        f.write(f'OPENAI_API_KEY={openai_api_key}\n')
    #load_dotenv()
    return openai_api_key