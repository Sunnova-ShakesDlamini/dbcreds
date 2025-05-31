# Makefile for dbcreds

.PHONY: help install test lint docs clean

help:
	@echo "Available commands:"
	@echo "  make install    Install package in development mode"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linters"
	@echo "  make docs       Build documentation"
	@echo "  make serve-docs Serve documentation locally"
	@echo "  make clean      Clean build artifacts"

install:
	uv pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=dbcreds --cov-report=html --cov-report=term

lint:
	ruff check .
	black --check .
	mypy dbcreds

format:
	black .
	ruff check --fix .

docs:
	mkdocs build

serve-docs:
	mkdocs serve

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf site/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
