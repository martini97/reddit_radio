.DEFAULT_GOAL := lint
.PHONY: pyclean lint test install requirements requirements-dev

pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

lint: pyclean
	$(VENV)/black --check --diff reddit_radio tests
	$(VENV)/isort --check --diff .
	$(VENV)/flake8 reddit_radio tests

test: pyclean
	PYTHON_ENV=test $(VENV)/pytest -n 4 --cov=reddit_radio --cov-report=term-missing

install:
	$(VENV)/pip install -r requirements/requirements.txt \
		-r requirements/requirements-dev.txt

requirements: requirements/requirements.txt
requirements-dev: requirements/requirements-dev.txt

include Makefile.venv
