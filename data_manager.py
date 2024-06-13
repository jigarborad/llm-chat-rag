import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from css import styles

def pdf_uploader():
    # Uploading the PDF file
    #st.markdown(styles.upload_banner, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload The PDF file", type="pdf")
    if uploaded_file is not None:
        # Extract text from the uploaded PDF
        pdf_reader = PdfReader(uploaded_file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)

        # Split the extracted text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text=text)

        store_name = uploaded_file.name[:-4]
        vector_store_path = f"VectorStore_{store_name}"
        return vector_store_path, chunks, uploaded_file
    return "","",None