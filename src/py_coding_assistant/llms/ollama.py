from typing import Tuple

import ollama
from ollama import ChatResponse, Client, chat

from .base import LLM


class OllamaLLM(LLM):
    """
    Ollama LLM implementation
    """

    def __init__(
        self,
        model_name: str,
    ):
        # call the parent class constructor to initialize
        super().__init__()

        self.model_name = model_name
        self._download_model_if_necessary(model_name)
        self.client = Client()

    def _download_model_if_necessary(self, model_name: str):
        """
        Downloads the `model_name` model if it is not already downloaded.
        """
        models_in_disk = [model.model for model in ollama.list().models]
        if self.model_name not in models_in_disk:
            print(f'Model {self.model_name} not found in disk, downloading...')
            ollama.pull(self.model_name)

    def generate_response(self, prompt: str) -> Tuple[str, dict[str, str]]:
        """
        Generates a response to the given prompt, given the current conversation history.

        It returns the response and the updated conversation history.
        """
        if self.system_prompt is None:
            raise ValueError('System prompt is not set')

        # concat the system prompt and the user message into a single message
        # and add the user message to the conversation history
        # Why not passing a system prompt instead?
        # Qwen-2.5-Coder-7B-Instruct does not work well with system prompts.
        # The model is built on Qwen's instruction-tuning approach which handles prompts
        # differently from models like GPT or Claude.
        # This is why we pass the system prompt as part of the user message.
        self.messages.append(
            {
                'role': 'user',
                'content': self.system_prompt + '\n' + prompt,
            }
        )

        response: ChatResponse = chat(
            model=self.model_name,
            messages=self.messages,
            stream=False,
        )
        response: str = response.message.content

        # add the response to the conversation history
        self.messages.append(
            {
                'role': 'assistant',
                'content': response,
            }
        )

        return response, self.messages
