from langchain_core.prompts import ChatPromptTemplate

def prompt():
    return ChatPromptTemplate.from_template("""
                Answer the question based only on the provided context below. 
                If the context doesnot contain enough information to answer say i dont know 
                rather than guessing or using outside knowledge

                Context: {context}

                Question: {input}
                                                                
                Answer: """
            )
