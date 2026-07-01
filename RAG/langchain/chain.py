#from python-dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables.base import Runnable
from langchain_core.output_parsers import StrOutputParser
 

#load_dotenv()  # Load environment variables from .env file

llm = ChatOllama(model="llama3")
print(isinstance(llm, Runnable))
system_llm = SystemMessage(content="You are a helpful assistant that answers questions about the devops.")
prompt = HumanMessage(content="Hello, what is the capital of France?") 
print(isinstance(prompt, Runnable))

parser = StrOutputParser()
chain = llm | parser
response= chain.invoke([prompt])
print(response)

# Executable order when we call invoke() on the chain:
# HumanMessage = raw material (input)
# llm = machine 1
# StrOutputParser = machine 2
# invoke() = turns the conveyor belt on

Chain2=llm | parser
response2=Chain2.invoke([HumanMessage(content="What is the capital of Germany?")])
print(response2)

chain3=Chain2 | chain
response3=chain3.invoke([HumanMessage(content="What is the capital of Italy?")])
print(response3)

chain4= Chain2 | chain3 | parser
response4=chain4.invoke([HumanMessage(content="What is the capital of India?")])
print(response4)

chain5= chain4 | parser
response5=chain5.invoke([HumanMessage(content="What is the capital of Japan?")])
print(response5)

chain6= llm  | parser
response6=chain6.invoke([SystemMessage(content="You are a helpful assistant that answers questions about the devops."), HumanMessage(content="Explain about docker and kubernetes?")])
print(response6)

# Runnable expects input as llm([HumanMessage(content="What is the capital of France?")]) and returns a list of messages.
# Return AIMesage object, which is a subclass of BaseMessage. The content of the message can be accessed using the content attribute.

# llm ------------> Parser ------------>
#      AIMessages            String



response7 = llm.invoke("Hello")

print(type(response7))
print(response7)
print(response7.content)