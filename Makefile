.DEFAULT_GOAL := help

.PHONY: help install install-dev lint format test agent dbt-run dbt-test dbt-docs clean

help: ## show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## install production dependencies
	pip install -r requirements.txt

install-dev: ## install development dependencies
	pip install -r requirements.txt -r requirements-dev.txt

lint: ## check code style and logic errors
	ruff check agent/

format: ## auto-format code
	ruff format agent/

test: ## run tests with coverage
	pytest

agent: ## start the telemetry collection agent
	python -m agent.main

dbt-run: ## run all dbt models
	cd transform && dbt run

dbt-test: ## run dbt tests
	cd transform && dbt test

dbt-docs: ## generate and serve dbt documentation
	cd transform && dbt docs generate && dbt docs serve

clean: ## remove temporary and generated files
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -type d -name .ruff_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".coverage" -delete
