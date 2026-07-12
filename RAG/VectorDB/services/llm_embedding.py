from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings

def get_llm_model():
    llm = ChatOllama(model="llama3")
    return llm


def get_ollama_embedding():
    embedding = OllamaEmbeddings(model="nomic-embed-text")
    #print(embedding.embed_query("Hello"))
    return embedding