import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from dotenv import load_dotenv, set_key
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="LLM Chat App", page_icon=":robot_face:", layout="centered")

# Custom CSS for complete redesign
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Helvetica Neue', sans-serif;
            color: #333;
        }
        .main {
            background: linear-gradient(to right, #ece9e6, #ffffff);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stTextInput>div>div>input {
            border-radius: 5px;
            border: 1px solid #ccc;
            padding: 10px;
            width: 100%;
        }
        .stButton>button {
            background-color: #2e7bcf;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #1e5bbf;
        }
        .sidebar .sidebar-content {
            background-color: #2e7bcf;
            color: white;
        }
        .sidebar .sidebar-content a {
            color: white;
        }
        h1 {
            color: #2e7bcf;
        }
        .card {
            background-color: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stSpinner {
            border-top-color: #2e7bcf;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar contents
with st.sidebar:
    st.title("LLM Chat App")
    st.markdown('''
                Welcome to the LLM Chat App! Please enter your name and start chatting.
                ## About the app
                The app is powered by:
                - Streamlit
                - LangChain
                - OpenAI
                ''')
    add_vertical_space(5)
    st.write("Made with ❤️ by [Jigar](https://github.com/jigarborad)")


def chat_with_llm():
    # Check if OpenAI API key exists in .env
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not openai_api_key:
        openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")
        if openai_api_key:
            with open('.env', 'a') as f:
                f.write(f'OPENAI_API_KEY={openai_api_key}\n')
            load_dotenv()
            chat_with_llm()
            #st.experimental_rerun()  # Rerun the app to reload with the new API key

    else:
        # Uploading the PDF file
        uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
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

            # Load or create a vector store
            vector_store_path = f"VectorStore_{store_name}"
            if os.path.exists(vector_store_path):
                VectorStore = FAISS.load_local(vector_store_path, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
            else:
                embeddings = OpenAIEmbeddings()
                VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
                VectorStore.save_local(vector_store_path)

            st.success(f'PDF "{uploaded_file.name}" uploaded and processed successfully!')

            # Input for the query
            query = st.text_input("Shoot your question related to the PDF")

            if query:
                # Perform similarity search and get the response
                with st.spinner("Processing your query..."):
                    docs = VectorStore.similarity_search(query=query, k=2)
                    chain = load_qa_chain(llm=ChatOpenAI(model_name="gpt-3.5-turbo"), chain_type="stuff")
                    with get_openai_callback() as cb:
                        response = chain.invoke(input={"input_documents": docs, "question": query})["output_text"]
                        print(cb)
                st.markdown(f'<div class="fade-in">{response}</div>', unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="fade-in">Chat with LLM &#x1F916;</h1>', unsafe_allow_html=True)

    st.markdown("""
        <div class="card fade-in">
            <h2>Upload your PDF</h2>
            <p>Upload a PDF file and ask questions related to its content.</p>
        </div>
    """, unsafe_allow_html=True)
    chat_with_llm()
    

if __name__ == "__main__":
    main()
