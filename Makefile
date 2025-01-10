cli-with-dummy-model:
	uv run python cli.py \
		--source-code-path ./src/py_coding_assistant \
		--agent-type single-llm \
		--llm-provider dummy

cli-with-qwen:
	uv run python cli.py \
		--source-code-path ./src/py_coding_assistant \
		--agent-type single-llm \
		--llm-provider ollama \
		--llm-model qwen2.5-coder:7b-instruct

cli-with-claude:
	uv run python cli.py \
		--source-code-path ./src/py_coding_assistant \
		--agent-type single-llm \
		--llm-provider anthropic \
		--llm-model claude-3-5-sonnet-20241022

lint:
	ruff check .

format:
	ruff format .
