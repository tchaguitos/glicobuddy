run:
	uvicorn main:app --reload

test:
	pytest -vv contextos/ tests/

coverage:
	pytest --cov=contextos/ --cov-fail-under=90

coverage-report:
	pytest contextos/ tests/ --cov=. --cov-report html --cov-append --disable-warnings
