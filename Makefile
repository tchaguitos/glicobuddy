run:
	uvicorn main:app --reload

test:
	pytest -vv tests/

coverage:
	pytest --cov=tests/

coverage-report:
	pytest tests --cov=. --cov-report html --cov-append --disable-warnings
