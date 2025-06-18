# Makefile for Dungeon Master development

.PHONY: help install install-dev clean test lint format type-check build check-dist publish-test publish release

# Default target
help:
	@echo "Available targets:"
	@echo "  help        - Show this help message"
	@echo "  install     - Install production dependencies"
	@echo "  install-dev - Install development dependencies"
	@echo "  clean       - Clean up build artifacts and cache"
	@echo "  test        - Run tests with coverage"
	@echo "  lint        - Run linting checks"
	@echo "  format      - Format code with black and isort"
	@echo "  type-check  - Run mypy type checking"
	@echo "  build       - Build the package"
	@echo "  check-dist  - Check package distribution"
	@echo "  publish-test- Publish to Test PyPI"
	@echo "  publish     - Publish to PyPI (requires authentication)"
	@echo "  release     - Prepare release (clean, build, check)"

# Installation targets
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

# Clean up
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Testing
test:
	pytest --cov=dungeon_master --cov-report=html --cov-report=term-missing

# Code quality
lint:
	flake8 dungeon_master tests
	black --check dungeon_master tests
	isort --check-only dungeon_master tests

format:
	black dungeon_master tests
	isort dungeon_master tests

type-check:
	mypy dungeon_master

# Build and publish
build:
	python -m build

check-dist: build
	twine check dist/*

publish-test: build check-dist
	twine upload --repository testpypi dist/*

publish: build check-dist
	twine upload dist/*

release: clean build check-dist
	@echo "Building release for cursor-dungeon-master..."
	@echo "Version: $(shell grep version pyproject.toml | head -1 | sed 's/.*= *"\(.*\)".*/\1/')"
	@echo "Ready to publish to PyPI. Run 'make publish' to proceed."

# Development setup
dev-setup: install-dev
	@echo "Development environment set up successfully!"
	@echo "Run 'make test' to run tests"
	@echo "Run 'make lint' to check code quality"
	@echo "Run 'make format' to format code" 