import os
import logging
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services import llm_embedding

logger = logging.basicConfig( datefmt= "%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

dir = "C://Users//santhi.bhogavalli//github//GenAi-practise//RAG//VectorDB//education_text_corpus"
file_pattern = "**/*.txt"
vdb = "C://Users//santhi.bhogavalli//github//GenAi-practise//RAG//VectorDB//chroma_db"
os.makedirs(vdb, exist_ok=True)

def ingest():
    logger.info("Load and split")
    docs = load_split()
    print(len(docs))
    logger.info("Attach document level medatadata")
    for doc in docs:
        filename = doc.metadata["source"].split("\\")[-1]
        doc.metadata["topic"] = filename.replace(".txt", "")
    #vector_store(docs,persistence_dir) commenting this to load few
    vectore_store_batch(docs,vdb)

def load_split():
    logger.info("Loading directory and searching files with %s",file_pattern)
    Loader = DirectoryLoader(dir, glob=file_pattern,loader_cls=TextLoader)
    logger.info("Spliting text data by chuncking.")
    split = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap = 5)
    load = Loader.load_and_split(split)
    return load



def vector_store(docs,vdb):
    logger.info("Iniating Embedding")
    embedding = llm_embedding.get_ollama_embedding()
    logger.info("load data to chromadb from embeddings")
    vdb = Chroma.from_documents(documents=docs[:5], #testing with first 5 doc
                                embedding=embedding, 
                                persist_directory=vdb,
                                collection_name="education_text_corpus")
    print(vdb)

#to avoid multiple data tokeniztion issue we should use batch  to load at once
def vectore_store_batch(docs,vdb):
    embedding = llm_embedding.get_ollama_embedding()
    db = Chroma(embedding_function= embedding,
                persist_directory=vdb,
                collection_name="education_text_corpus_batch")
    
    BATCH_SIZE = 200
    for i in range(0, len(docs), BATCH_SIZE):
        batch = docs[i:i + BATCH_SIZE]

        db.add_documents(batch)

        logger.info(f"Loaded {i + len(batch)} / {len(docs)}")



