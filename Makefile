# Convenience targets. See README.md for details.

.PHONY: setup dashboard run test lint

setup:            ## Install the Python environment
	uv sync

dashboard:        ## Build the live dashboard frontend (needs Node.js)
	npm --prefix dashboard install
	npm --prefix dashboard run build

run:              ## Run the sample experiment with the live dashboard
	uv run python __main__.py

test:
	uv run python -m pytest

lint:
	git ls-files '*.py' | xargs uv run pylint --rcfile=.pylintrc
