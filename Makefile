.PHONY: run lint

run:
	python main.py

lint:
	uv run black src