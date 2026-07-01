import chatbot
import logging
#import click

logging.basicConfig(level=logging.INFO)

# @click.command()
# @click.option('-q', '--question', required=True, help='Question to ask the assistant.')
# @click.option('-t', '--topic', help='Assistant prompt  example: specific topic provide topic name like devops/countries/cities/chef_recipes.')
# @click.option('-s', '--system_prompt', default="You are a helpful assistant that answers questions about the {topic}.", help='System prompt for the assistant.')

def main():
    logging.info("Hello from langchain!")
    #chatbot.run(question=question, topic=topic, system_prompt=system_prompt)
    chatbot.run()

if __name__ == "__main__":
    main()
