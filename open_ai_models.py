import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

class OpenAIModel:
    def __init__(self, api_key):
        self.api_key = api_key
        self.available_models = ["gpt-3.5-turbo"]

    def get_available_models(self):
        return self.available_models

    def open_ai_embedding(self, vector_store_path, chunks):
        embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        vector_store_full_path = f"VectorStore_{vector_store_path[:-4]}_openaiembeddings"
        if os.path.exists(vector_store_full_path):
            VectorStore = FAISS.load_local(vector_store_full_path, embeddings, allow_dangerous_deserialization=True)
        else:
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            VectorStore.save_local(vector_store_full_path)
        return VectorStore

    def query_model(self, model_name, query, VectorStore, history):
        if model_name not in self.available_models:
            raise ValueError("Model not available")
        docs = VectorStore.similarity_search(query=query, k=2)
        chain = load_qa_chain(llm=ChatOpenAI(model_name=model_name, openai_api_key=self.api_key), chain_type="stuff")
        
        # Combine history and current query for the model input
        input_text = "\n".join([f"{h['role']}: {h['content']}" for h in history]) + f"\nuser: {query}"
        
        with get_openai_callback() as cb:
            response = chain.invoke(input={"input_documents": docs, "question": input_text})["output_text"]
        return response
