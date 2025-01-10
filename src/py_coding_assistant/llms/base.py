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
        # self.messages = [{
        #     'role': 'system',
        #     'content': system_prompt,
        # }]


class LLMFactory:
    """
    Factory class for creating LLMs.
    """

    @staticmethod
    def create_llm(
        llm_provider: LLMProviderType,
        llm_model: str | None = None,
    ) -> LLM:
        if llm_provider == LLMProviderType.OLLAMA:
            from .ollama import OllamaLLM

            return OllamaLLM(llm_model)
        elif llm_provider == LLMProviderType.DUMMY:
            from .dummy import DummyLLM

            return DummyLLM()
        elif llm_provider == LLMProviderType.ANTHROPIC:
            from .anthropic import AnthropicLLM

            return AnthropicLLM(llm_model)
        else:
            raise ValueError(f'Invalid LLM provider: {llm_provider}')
