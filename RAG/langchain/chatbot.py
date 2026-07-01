from langchain_core.messages import HumanMessage, SystemMessage 
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import click
import logging

logging.basicConfig(level=logging.INFO)

def run(question=None, topic=None, system_prompt="You are a helpful assistant that answers questions about the {topic}."):
        while not question:
            try:
                question = input(f"Please enter your question?: ")
                llm = ChatOllama(model="llama3")
                logging.info(f"Initialized ChatOllama with model: {llm.model}")
                system_prompt = system_prompt.format(topic=topic) if topic else system_prompt
                logging.info(f"Using system prompt: {system_prompt}")
                system = SystemMessage(content=system_prompt)
                prompt = HumanMessage(content=question)
                parser = StrOutputParser()
                chain = llm | parser
                logging.info(f"Executing with question: {question}")
                response = chain.invoke([system, prompt])
                logging.info(f"Received response: {response}")
                if question.lower() == "exit" or question.lower() == "quit":
                    break
                elif question.lower() == "clear":
                    logging.info("Clearing the console...")
                    click.clear()
                    continue
                return response
            except Exception as e:
                logging.error(f"Error occurred: {e}")
            return "Sorry, I encountered an error while processing your request."

# @click.command()
# @click.option('-q', '--question', required=True, help='Question to ask the assistant.')
# @click.option('-s', '--system_prompt', default="You are a helpful assistant that answers questions about the devops.", help='System prompt for the assistant.')
# def main(question, system_prompt):
#     response = run(question, system_prompt)
#     print(response)

# if __name__ == "__main__":
#     main()