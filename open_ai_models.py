import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.callbacks import get_openai_callback

def open_ai_embedding(vector_store_path, chunks, openai_api_key):
    embeddings = OpenAIEmbeddings(openai_api_key= openai_api_key)
    if os.path.exists(vector_store_path):
        VectorStore = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
    else:
        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        VectorStore.save_local(vector_store_path)
    return VectorStore

def gpt_turbo_3_5(query, VectorStore,openai_api_key):
    docs = VectorStore.similarity_search(query=query, k=2)
    chain = load_qa_chain(llm=ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key= openai_api_key), chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.invoke(input={"input_documents": docs, "question": query})["output_text"]
        print(cb)
    return response

