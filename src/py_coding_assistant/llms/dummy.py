from typing import Tuple

from .base import LLM


class DummyLLM(LLM):
    """
    Dummy LLM implementation useful for quick debugging.
    """

    def __init__(self):
        # call the parent class constructor to initialize
        super().__init__()

    def generate_response(self, prompt: str) -> Tuple[str, dict[str, str]]:
        """
        Generates a dummy (and fast) response to the given prompt.
        """
        response = 'Dummy response!'

        self.messages.append(
            {
                'role': 'assistant',
                'content': response,
            }
        )

        return response, []
