from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from services import vector_validation
from ingest import vectordb_ingest
from prompts.rag_prompt import prompt


llm = ChatOllama(
    model="llama3"
)


def format_docs(docs):

    return "\n\n".join(
        doc.page_content
        for doc in docs
    )


def initialize():

    print("=" * 60)
    print("Initializing RAG")
    print("=" * 60)

    if not vector_validation.vector_exists():

        print("Vector DB not found.")

        print("Starting ingestion...")

        vectordb_ingest.ingest()

        print("Finished building vector database.")

    else:

        print("Existing Vector DB found.")

    vector = vector_validation.load_vector_store()

    retriever = vector.as_retriever()

    return retriever


def ask_question(retriever):
    rag_prompt = prompt()

    chain = (
                rag_prompt | 
                llm | 
                StrOutputParser()
            )

    while True:

        question = input("\nQuestion (type exit): ")

        if question.lower() == "exit":

            break

        docs = retriever.invoke(question)

        context = format_docs(docs)

        #print(context)

        answer = chain.invoke({

            "context": context,

            "input": question

        })

        print("\nAnswer\n")

        print(answer)


def main():

    retriever = initialize()
    print(retriever)
    ask_question(retriever)


if __name__ == "__main__":

    main()