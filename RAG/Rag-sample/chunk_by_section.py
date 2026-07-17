import logging, re, datetime
import os
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

logger.info("This is to extract data from pdf")

# Initalize the pdf file here
def initialize(pdf_name="chapter1.pdf",
               image_folder="images",
               text_folder="text",
               json_file="save_image_metadata.json"):

    pdf_path = os.path.join("c:\\Users\\santhi.bhogavalli\\github\\GenAi-practise\\RAG\\Rag-sample\\Maths-Book", pdf_name)
    image_folder= os.path.join("c:\\Users\\santhi.bhogavalli\\github\\GenAi-practise\\RAG\\Rag-sample\\Maths-Book", image_folder)
    text_folder = os.path.join("c:\\Users\\santhi.bhogavalli\\github\\GenAi-practise\\RAG\\Rag-sample\\Maths-Book", text_folder)
    json_file = os.path.join("c:\\Users\\santhi.bhogavalli\\github\\GenAi-practise\\RAG\\Rag-sample\\Maths-Book",json_file)
    
    logger.info(f"Opening pdf_file: {pdf_path}")
    doc = pymupdf.open(pdf_path)

    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(text_folder, exist_ok=True)

    return doc, image_folder, text_folder, json_file

# Extract_chapter
def get_full_text(doc):
    """
    Combine all pages into a single string.
    """

    pages = []

    for page in doc:
        pages.append(page.get_text("text"))

    return "\n".join(pages)

def splitting(doc):
    """
    Extract all page text, combine into one string,
    then split into chunks.
    """

    logger.info("Extracting pages...")

    pages = get_full_text(doc)

    # Matches:
    # 1.1
    # 1.2
    # 12.3
    # 15.10

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=75, #(15% of chunk_size. ideally it should be 10–20% of chuk_size)
        separators=[r"(?=^\d+(?:\.\d+)+\s+.*)",
            "\n\n",
            "\n"
        ],
        is_separator_regex= True
    )
    all_chunks = []
    logger.info("Number of pages: %d", len(pages))
    chunk = splitter.split_text(pages)
    for index, chunk in enumerate(chunk, start=1):
        all_chunks.append(
            Document(
                page_content=chunk,
                metadata= {
                    "chunk": index,
                    "source": "chapter1.pdf"
                }
            )
        )
       
    logger.info("Generated %d chunks", len(all_chunks))
    
    return all_chunks

if __name__ == "__main__":
    doc, image_folder, text_folder, json_file = initialize()

    splitting(doc)

    doc.close()