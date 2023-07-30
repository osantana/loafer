.PHONY: clean-pyc

default: test

clean-pyc:
	@find . -iname '*.py[co]' -delete
	@find . -iname '__pycache__' -delete
	@find . -iname '.coverage' -delete
	@rm -rf htmlcov/

clean-dist:
	@rm -rf dist/
	@rm -rf build/
	@rm -rf *.egg-info

clean: clean-pyc clean-dist

test:
	poetry run pytest -vv tests

test-cov:
	poetry run pytest -vv --cov=loafer tests

check-fixtures:
	poetry run pytest --dead-fixtures

dist: clean
	poetry build

release: dist
	git tag `poetry version -s`
	git push origin `poetry version -s`
	poetry publish
