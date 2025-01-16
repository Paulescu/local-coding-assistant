from textual import on, work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Footer, Header, Input, Markdown

from py_coding_assistant.agents import AgentFactory, AgentType
from py_coding_assistant.llms import LLMProviderType
from py_coding_assistant.repo import Repo


class Prompt(Markdown):
    pass


class Response(Markdown):
    BORDER_TITLE = 'AI Coding assistant'


class CodingAssistantApp(App):
    AUTO_FOCUS = 'Input'

    CSS = """
    Prompt {
        background: $primary 10%;
        color: $text;
        margin: 1;
        margin-right: 8;
        padding: 1 2 0 2;
    }

    Response {
        border: wide $success;
        background: $success 10%;
        color: $text;
        margin: 1;
        margin-left: 8;
        padding: 1 2 0 2;
    }
    """

    def __init__(self):
        super().__init__()

        # TODO: Make these configurable
        self.agent_type = AgentType.SINGLE_LLM
        self.llm_provider = LLMProviderType.OLLAMA
        self.llm_model = 'qwen2.5-coder:1.5b-instruct'  # "qwen2.5-coder:7b-instruct"
        self.source_code_path = './src/py_coding_assistant'

    def compose(self) -> ComposeResult:
        yield Header()
        with VerticalScroll(id='chat-view'):
            yield Response(
                f'I am your {self.llm_model} coding assistant. How can I help you?'
            )
        yield Input(placeholder='How can I help you?')
        yield Footer()

    def on_mount(self) -> None:
        # Load the repo
        self.repo = Repo(self.source_code_path)

        # Create the agent
        self.agent = AgentFactory.create_agent(
            agent_type=self.agent_type,
            llm_provider=self.llm_provider,
            llm_model=self.llm_model,
            repo=self.repo,
        )

    @on(Input.Submitted)
    async def on_input(self, event: Input.Submitted) -> None:
        chat_view = self.query_one('#chat-view')
        event.input.clear()

        await chat_view.mount(Prompt(event.value))
        await chat_view.mount(response := Response())
        response.anchor()

        if event.value == 'exit':
            # terminate the app, no need to bother the agent
            self.exit()

        self.send_prompt(event.value, response)

    @work(thread=True)
    def send_prompt(self, prompt: str, response: Response) -> None:
        """
        Spawns a thread to send the prompt to the agent and update the response.
        """
        response_content = ''
        # llm_response = self.model.prompt(prompt, system=SYSTEM)
        llm_response = self.agent.generate_response(prompt)
        for chunk in llm_response:
            response_content += chunk
            self.call_from_thread(response.update, response_content)


if __name__ == '__main__':
    app = CodingAssistantApp()
    app.run()
