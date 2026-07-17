import os
import logging
from services import llm_embedding
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate

logger = logging.basicConfig('%(asctime)s | %(levelname)s | %(messages)s', level=logging.INFO)
logger = logger.get_logger(__name__)

dir = "C://Users//santhi.bhogavalli//github//GenAi-practise//RAG//VectorDB//education_text_corpus"
file_pattern = "**/*.txt"
vdb = "C://Users//santhi.bhogavalli//github//GenAi-practise//RAG//VectorDB//faiss-db"
os.makedirs(vdb, exist_ok=True)


def load_split():
    logger.info("Loading directory and searching files with %s",file_pattern)
    Loader = DirectoryLoader(dir, glob=file_pattern,loader_cls=TextLoader)
    logger.info("Spliting text data by chuncking.")
    split = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap = 5)
    load = Loader.load_and_split(split)
    return load

def faiss_vdb():
    vector_db = FAISS.from_documents(documents=load_split(),embedding=llm_embedding.get_ollama_embedding())
    vector_db.save_local("faiss_index")
    logger(f"verctor db of {faiss_vdb}")
    vector_db = FAISS.load_local("faiss_index",
                                 llm_embedding.get_ollama_embedding(),
                                 allow_dangerous_deserialization=True)
    return vector_db

def retriver():
    vdb = faiss_vdb()
    retriever_data = vdb.as_retriever(
    search_kwargs={
        "k":4
    }
    )
    return retriever_data
    
def prompt():
    data = ChatPromptTemplate.from_messages(
        [
            ("system", """
                    You are expert of reading data from vector database 
                    where i have loaded a mathmatics textbook from NCERT
                """
            ),
            ("human", """"
                    contex : {Contex} 
                    Question : {question}
                """
            )
        ]
    )
    return data

if __name__ == "__main__":
    
