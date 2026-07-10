Langchain Document: https://docs.langchain.com
In Langchain we have to us core and community as a begginer i'm so confusied about this.
Langchain_core : Officail stable package maintined by Langchain team and it contains fundamental abstractions(documents, textsplitters, retrivers,chain)
 Ex: 
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter

Langchain_community: This is Extension ecosystem maintained by contributers outside of core team. It integrates with external tools, API's, DataBases
Ex: 
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_community.vectorstores import FAISS

