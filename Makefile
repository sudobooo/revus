package-install:
	pip install --user --force-reinstall dist/*.whl --break-system-packages

lint:
	poetry run ruff check .

lint-fix:
	poetry run ruff check --fix .