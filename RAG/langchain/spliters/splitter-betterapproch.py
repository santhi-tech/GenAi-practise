import os
from langchain_community.document_loaders import ( TextLoader,
                                                  PyPDFLoader,
                                                  CSVLoader)
from langchain_text_splitters import RecursiveCharacterTextSplitter

folder = r"C:\Users\santhi.bhogavalli\Downloads"
LOADERS = {
    ".txt": TextLoader,
    ".pdf": PyPDFLoader,
    ".csv": CSVLoader
}


def load_document(path):

    extension = os.path.splitext(path)[1]

    if extension == ".txt":
        return TextLoader(
            path,
            autodetect_encoding=True
        )

    elif extension == ".pdf":
        return PyPDFLoader(path)

    elif extension == ".csv":
        return CSVLoader(path)

    return None

split = RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=0, separators=["","\n","\n\n"])

for file in os.listdir(folder):
    full_path = os.path.join(folder, file)
    loader = load_document(full_path)
    if loader is None:
        continue
    docs = loader.load_and_split(split)
    print(docs[0].page_content)