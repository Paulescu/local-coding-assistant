from abc import ABC, abstractmethod
from enum import Enum


class LLMProviderType(Enum):
    OLLAMA = 'ollama'
    DUMMY = 'dummy'
    ANTHROPIC = 'anthropic'


class LLM(ABC):
    """
    Common interface for all LLMs, no matter the provider.
    """

    def __init__(self):
        self.system_prompt = None
        self.messages = []

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass

    def set_system_prompt(self, system_prompt: str):
        """
        Sets the initial system prompt that instructs the LLM to behave in a certain way.
        """
        self.system_prompt = system_prompt
