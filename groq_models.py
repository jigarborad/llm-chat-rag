import os
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from groq import Groq

class GroqModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.available_models = ["llama3-70b-8192", "mixtral-8x7b-32768", "llama3-8b-8192"]

    def get_available_models(self):
        return self.available_models

    def local_embedding(self, vector_store_path, chunks):
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store_full_path = f"VectorStore_{vector_store_path[:-4]}_huggingfaceembeddings"
        if os.path.exists(vector_store_full_path):
            VectorStore = FAISS.load_local(vector_store_full_path, embeddings, allow_dangerous_deserialization=True)
        else:
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            VectorStore.save_local(vector_store_full_path)
        return VectorStore

    def query_model(self, model_name, query, VectorStore, history, template):
        if model_name not in self.available_models:
            raise ValueError("Model not available")
        docs = VectorStore.similarity_search(query=query, k=3)
        chain = load_qa_chain(llm=ChatGroq(model_name=model_name, api_key=self.api_key), chain_type="stuff")
        prompt = PromptTemplate(template=template, input_variables=["history", "query"])
        input_text = prompt.format(history="\n".join([f"{h['role']}: {h['content']}" for h in history]), query=query)
        
        response = chain.invoke(input={"input_documents": docs, "question": input_text})["output_text"]
        return response

    def transcription_model(self, audio):
        client = Groq(api_key=self.api_key)
        with open("microphone-results.wav", "wb") as f:
            f.write(audio.get_wav_data())

        # Use Groq API for transcription
        with open("microphone-results.wav", "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
            file=("microphone-results.wav", audio_file),
            model="whisper-large-v3",
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0  # Optional
        )
        return transcription