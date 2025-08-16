lint:
	uv run ruff check

fmt:
	uv run ruff format

fix:
	uv run ruff format 
	uv run ruff check --fix --unsafe-fixes