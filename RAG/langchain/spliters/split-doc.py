from langchain_community.document_loaders import PyPDFLoader,TextLoader,csv_loader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
file_path_dir = "C:\\Users\\santhi.bhogavalli\\Downloads\\"
file_pattern = [".txt",".pdf",".csv",".xlsx"]
files=[]
for file in os.listdir(file_path_dir):
    import os


for file in os.listdir(file_path_dir):
    full_path = os.path.join(file_path_dir, file)

    if file.endswith(".txt"):
        text = TextLoader(full_path, autodetect_encoding=True).load()
        print(text[0].metadata)

    elif file.endswith(".pdf"):
        pdf = PyPDFLoader(full_path).load()
        print(len(pdf))

    elif file.endswith(".csv"):
        print("Use CSVLoader")
        csv = csv_loader.CSVLoader(full_path).load()
        print(csv[0].page_content)

    # # elif file.endswith(".xlsx"):
    # #     print("Use UnstructuredExcelLoader")
                 
    
split = RecursiveCharacterTextSplitter(separators=True)
print(split)
