import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

class DataManager:
    @staticmethod
    def pdf_uploader():
        # Initialize session_state if not already done
        if 'uploaded_file' not in st.session_state:
            st.session_state.uploaded_file = None

        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
        
        # Check if a new file has been uploaded
        if uploaded_file and uploaded_file != st.session_state.uploaded_file:
            st.session_state.uploaded_file = uploaded_file  # Update session_state
        
        if uploaded_file is not None:
            pdf_reader = PdfReader(uploaded_file)
            text = "".join(page.extract_text() for page in pdf_reader.pages)
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            chunks = text_splitter.split_text(text=text)
            return uploaded_file.name, chunks, uploaded_file
        
        return None, [], None
