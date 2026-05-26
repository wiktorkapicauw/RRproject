.PHONY: build run format lint

# Build the Docker image
build:
	docker compose build

# Run the application container
run:
	docker compose run --rm app

# Format Python code using black and isort
format:
	.venv/bin/black src main.py
	.venv/bin/isort src main.py

# Lint Python code using flake8
lint:
	.venv/bin/flake8 src main.py
