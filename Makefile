.DEFAULT_GOAL := ci
.PHONY: pyclean ci

pyclean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

ci: pyclean
	$(VENV)/black --check --diff reddit_radio
	$(VENV)/isort --check --diff reddit_radio
	$(VENV)/flake8 reddit_radio

requirements: requirements/requirements.txt
requirements-dev: requirements/requirements-dev.txt

include Makefile.venv
include requirements/Makefile
