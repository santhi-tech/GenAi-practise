from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings
import base64
import logging

logging.basicConfig(level=logging.INFO, format= "%(asctime)s | %(levelname)s | %(message)s" )

logger = logging.getLogger(__name__)



def get_model_llm():
    return OllamaLLM(model="llama3")

def get_embedding():
    return OllamaEmbeddings(model="nomic-embed-text")

def convert_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()
