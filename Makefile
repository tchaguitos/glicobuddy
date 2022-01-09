run:
	uvicorn main:app --reload

test:
	pytest -vv tests/

coverage:
	pytest --cov=contextos/ tests/
