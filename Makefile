run:
	uvicorn main:app --reload

test:
	pytest -vv tests/

shell:
	python3 -i main.py

coverage:
	pytest --cov=libs/ --cov=contextos/ --cov-fail-under=90

coverage-report:
	pytest contextos/ libs/ tests/ --cov=. --cov-report html --cov-append --disable-warnings

remove-coverage-report:
	rm -rf htmlcov
