# entrypoint.py
import getpass
from typing import Annotated

import typer
from dotenv import find_dotenv, load_dotenv
from loguru import logger

from py_coding_assistant.agents import AgentFactory, AgentType
from py_coding_assistant.llms import LLMProviderType
from py_coding_assistant.repo import Repo

# load environment variables
load_dotenv(find_dotenv())


def main(
    source_code_path: Annotated[
        str, typer.Option(help='The path to the source code to be analyzed')
    ],
    agent_type: Annotated[AgentType, typer.Option(help='The type of agent to use')],
    llm_provider: Annotated[
        LLMProviderType, typer.Option(help='The LLM provider to use')
    ],
    llm_model: Annotated[str, typer.Option(help='The LLM model to use')] = None,
):
    logger.add('logs/debug.log', rotation='500 MB')
    logger.debug('Starting the AI coding assistant')

    username = getpass.getuser()
    print(
        f'Hello, {username}! I am your AI coding assistant. How can I help you today?'
    )

    logger.debug('Loading the source code into Repo object')
    repo = Repo(source_code_path)
    logger.debug(f'Loaded {repo.file_count} files')

    logger.debug('Stringifying the repo')
    logger.debug(f'Characters in stringified repo: {len(repo.stringify()):,}')

    logger.debug('Loading the agent')
    agent = AgentFactory.create_agent(
        agent_type=agent_type,
        llm_provider=llm_provider,
        llm_model=llm_model,
        repo=repo,
    )

    logger.debug('Starting the chat loop')

    while True:
        user_input = input('> ')
        if user_input == 'exit':
            break
        else:
            # Generate a response from the agent
            response = agent.generate_response(user_input)
            print(f'🤖: {response}')


if __name__ == '__main__':
    typer.run(main)
