# Convenience targets. See README.md for details.

.PHONY: setup dashboard run test lint

setup:            ## Install the Python environment
	uv sync

dashboard:        ## Build the live dashboard frontend (needs Node.js)
	npm --prefix dashboard install --no-audit --no-fund --loglevel=error
	npm --prefix dashboard run build --silent
	@echo
	@echo "Dashboard built. It is served by the training process: run 'make run' and open the URL it prints."

run:              ## Run the sample experiment with the live dashboard
	uv run python __main__.py

test:
	uv run python -m pytest

lint:
	git ls-files '*.py' | xargs uv run pylint --rcfile=.pylintrc
