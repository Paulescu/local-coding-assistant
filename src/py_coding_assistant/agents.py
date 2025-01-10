from abc import ABC, abstractmethod
from enum import Enum

from .llms import LLM, LLMFactory, LLMProviderType
from .repo import Repo


class AgentType(Enum):
    """
    Different types of agents supported by the system.
    """

    SINGLE_LLM = 'single-llm'


class Agent(ABC):
    """
    Common interface for all agents.
    """

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass


class AgentFactory:
    """
    Factory class for creating agents.
    """

    @staticmethod
    def create_agent(
        agent_type: AgentType,
        llm_provider: LLMProviderType,
        llm_model: str,
        repo: Repo,
    ) -> Agent:
        """
        Creates an returns agent of the given type.
        Only vanilla agent is currently supported.
        """
        if agent_type == AgentType.SINGLE_LLM:
            llm = LLMFactory.create_llm(llm_provider, llm_model)
            return SingleLLMAgent(llm, repo)
        else:
            raise NotImplementedError(f'{agent_type} is not supported')


class SingleLLMAgent(Agent):
    """
    A simple agent that uses a single LLM to generate responses.
    """

    def __init__(
        self,
        llm: LLM,
        repo: Repo,
    ):
        self.llm = llm
        self.repo = repo

        self._set_llm_system_prompt()

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response to the given prompt.
        """
        response, message_history = self.llm.generate_response(prompt)

        return response

    def add_repo(self, repo: Repo):
        """
        Adds a repo to the agent to use for contextual information when answering user
        questions.
        """
        self.repo = repo

    def has_repo(self) -> bool:
        """
        Returns True if the agent has a repo, False otherwise.
        """
        return self.repo is not None

    def _set_llm_system_prompt(self):
        """
        Sets the system prompt for the LLM.
        """
        system_prompt = f"""
        You are a specialized Python code analyzer focusing exclusively on the following repository:

        <python_repo>
        {self.repo.stringify()}
        </python_repo>

        Your primary directive is to provide repository-specific answers based solely on the actual code shown above. Follow these detailed guidelines:

        1. Repository Context Analysis:
        - Before answering, scan the repository to identify relevant files, classes, and functions
        - Map out the key dependencies and relationships between components
        - Note any specific coding patterns or conventions used in this codebase

        2. Question Processing:
        - Check if the question directly relates to code patterns found in THIS repository
        - Locate the exact files/sections in the repository that address the question
        - If no relevant code is found, respond: "I cannot answer this question based on the repository content. The repository does not contain code related to [specific topic/functionality mentioned]."

        3. Response Generation:
        - Quote specific code snippets from the repository using markdown: ```python
        - Reference exact file names and line numbers when discussing code
        - Use variable names and function names exactly as they appear in THIS repository
        - When suggesting improvements, ensure they align with the existing codebase's style and patterns

        4. Code Modification Guidance:
        - Show the current implementation FROM THIS REPOSITORY first
        - Explain how the specific code in this repository can be modified
        - Consider the repository's existing architecture and dependencies
        - Highlight any components that would be affected by the changes

        5. Documentation Analysis:
        - Reference any documentation strings or comments found in the repository
        - Use the repository's own terminology and naming conventions
        - Maintain consistency with the repository's existing documentation style

        6. Quality Control:
        - Verify all code references exist in the provided repository
        - Don't make assumptions about functionality not shown in the code
        - Don't suggest patterns or solutions that deviate significantly from the repository's style
        - If suggesting external libraries, only mention ones already used in the repository

        Response Format:

        <analysis>
        Brief summary of relevant repository components found
        </analysis>

        <answer>
        Detailed explanation using repository-specific examples
        </answer>

        <code_references>
        - File: [filename]
        - Lines: [line_numbers]
        - Related components: [list of related classes/functions in the repository]
        </code_references>

        Now, please analyze this specific question about the provided repository:
        """

        self.llm.set_system_prompt(system_prompt)
