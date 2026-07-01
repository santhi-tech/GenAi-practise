# from dotenv import load_dotenv
from  langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

#load_dotenv()  # Load environment variables from .env file

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
prompt = HumanMessage(content="Hello, what is the capital of France?") 



def main():
    response = llm([prompt])
    print(response[0].content)  


if __name__ == "__main__":
    main()
