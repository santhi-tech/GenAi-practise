from langchain_core.messages import HumanMessage, SystemMessage 
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import click

def execute(question, system_prompt):
    try:
        llm = ChatOllama(model="llama3", role="user")
        system = SystemMessage(content=system_prompt)
        prompt = HumanMessage(content=question)
        parser = StrOutputParser()
        chain = llm | parser
    except Exception as e:
        print(f"Error occurred: {e}")
        return "Sorry, I encountered an error while processing your request."
    response = chain.invoke([system, prompt])
    return response

@click.command()
@click.option('-q', '--question', required=True, help='Question to ask the assistant.')
@click.option('-s', '--system_prompt', default="You are a helpful assistant that answers questions about the devops.", help='System prompt for the assistant.')
def main(question, system_prompt):
    response = execute(question, system_prompt)
    print(response)

if __name__ == "__main__":
    main()