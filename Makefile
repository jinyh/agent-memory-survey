PYTHON ?= uv run --active
PYTHON_DEV ?= uv run --active --extra dev

.PHONY: test lint refs eval agent

test:
	$(PYTHON_DEV) pytest tests/

lint:
	$(PYTHON_DEV) ruff check .

refs:
	$(PYTHON) python -m src.references

eval:
	$(PYTHON) python -m src.memory.evaluation --out docs/memory-eval/latest

agent:
	$(PYTHON) python -m src.memory.agent

docs:
	$(PYTHON) python scripts/check-doc-links.py
