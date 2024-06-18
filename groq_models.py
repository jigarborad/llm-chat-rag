import os
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

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

    def query_model(self, model_name, query, VectorStore, history):
        if model_name not in self.available_models:
            raise ValueError("Model not available")
        docs = VectorStore.similarity_search(query=query, k=3)
        chain = load_qa_chain(llm=ChatGroq(model_name=model_name, api_key=self.api_key), chain_type="stuff")
        
        # Combine history and current query for the model input
        input_text = "\n".join([f"{h['role']}: {h['content']}" for h in history]) + f"\nuser: {query}"
        
        response = chain.invoke(input={"input_documents": docs, "question": input_text})["output_text"]
        return response
