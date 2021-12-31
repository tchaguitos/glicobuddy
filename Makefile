test:
	pytest -vv tests/

coverage:
	pytest --cov=contextos/ tests/
