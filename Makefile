.PHONY: install test lint format coverage docs serve

install:
	pip install -r requirements.txt
	pip install pytest pre-commit coverage mkdocs mkdocs-material

test:
	pytest -q

lint:
	pre-commit run --all-files

format:
	black . && isort .

coverage:
	coverage run -m pytest && coverage report -m && coverage xml

docs:
	mkdocs build --strict

serve:
	mkdocs serve -a 0.0.0.0:8000
