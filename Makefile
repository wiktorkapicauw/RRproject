.PHONY: build run report format lint

build:
	docker compose build

run report:
	docker compose run --rm app

format:
	.venv/bin/black src main.py
	.venv/bin/isort src main.py

lint:
	.venv/bin/flake8 src main.py
