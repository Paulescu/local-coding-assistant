from .anthropic import AnthropicLLM
from .base import LLM, LLMProviderType
from .dummy import DummyLLM
from .ollama import OllamaLLM


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
            return OllamaLLM(llm_model)
        elif llm_provider == LLMProviderType.DUMMY:
            return DummyLLM()
        elif llm_provider == LLMProviderType.ANTHROPIC:
            return AnthropicLLM(llm_model)
        else:
            raise ValueError(f'Invalid LLM provider: {llm_provider}')
