.DEFAULT_GOAL := lint
CMD = poetry run
.PHONY: pyclean lint test install requirements requirements-dev

pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint: pyclean
	$(CMD) black --check --diff reddit_radio tests
	$(CMD) isort --check --diff .
	$(CMD) flake8 reddit_radio tests

test: pyclean
	PYTHON_ENV=test $(CMD) pytest -n 4 --cov=reddit_radio --cov-report=term-missing

install:
	poetry install

requirements: requirements/requirements.txt
requirements-dev: requirements/requirements-dev.txt
