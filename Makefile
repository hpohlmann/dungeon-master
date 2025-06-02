.PHONY: help install install-dev test test-coverage lint format type-check clean build upload demo

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install package
	pip install -e .

install-dev: ## Install package with development dependencies
	pip install -e .[dev]
	pre-commit install

test: ## Run tests
	pytest tests/ -v

test-coverage: ## Run tests with coverage report
	pytest tests/ -v --cov=dungeon_master --cov-report=html --cov-report=term

lint: ## Run linting
	flake8 dungeon_master/ hooks/ tests/
	black --check dungeon_master/ hooks/ tests/

format: ## Format code
	black dungeon_master/ hooks/ tests/

type-check: ## Run type checking
	mypy dungeon_master/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean ## Build package
	python setup.py sdist bdist_wheel

upload: build ## Upload package to PyPI
	twine upload dist/*

upload-test: build ## Upload package to Test PyPI
	twine upload --repository testpypi dist/*

package-install: build ## Install package from local build
	pip install dist/*.whl --force-reinstall

package-check: ## Check package metadata and structure
	python setup.py check
	twine check dist/*

demo: ## Run a demo of dungeon master
	@echo "=== Dungeon Master Demo ==="
	@echo "1. Initializing dungeon master..."
	python -m dungeon_master.cli init
	@echo "\n2. Listing all tracked files..."
	python -m dungeon_master.cli list --all
	@echo "\n3. Processing example file..."
	python -m dungeon_master.cli update examples/sample_service.py
	@echo "\n4. Showing generated context document..."
	@if [ -f "dungeon_master/auth_service.md" ]; then \
		echo "Generated context document:"; \
		echo "================================"; \
		cat dungeon_master/auth_service.md; \
	else \
		echo "No context document found."; \
	fi

check-all: lint type-check test ## Run all checks

dev-setup: install-dev ## Complete development setup
	@echo "Development environment setup complete!"
	@echo "You can now run:"
	@echo "  make demo     - See dungeon master in action"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Check code style" 