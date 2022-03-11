hooks_setup:
	pip install black flake8 isort[pyproject] pre-commit
	pre-commit install

run:
	docker-compose up --build

stop:
	docker-compose stop

shell:
	docker-compose run --rm app python manage.py shell

superuser:
	docker-compose run --rm app python manage.py createsuperuser

migrations:
	docker-compose run --rm app python manage.py makemigrations

migrate:
	docker-compose run --rm app python manage.py migrate
