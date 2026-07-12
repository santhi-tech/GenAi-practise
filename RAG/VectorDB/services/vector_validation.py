import os

from langchain_chroma import Chroma

from services import llm_embedding

DB_PATH = "./chroma_db"

COLLECTION = "education_text_corpus_batch"

_vector = None


def vector_exists():

    return os.path.exists(DB_PATH)


def load_vector_store():

    global _vector

    if _vector is None:

        _vector = Chroma(
            persist_directory=DB_PATH,
            collection_name=COLLECTION,
            embedding_function=llm_embedding.get_ollama_embedding(),
        )

    return _vector