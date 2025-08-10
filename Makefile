install:
	uv sync

collectstatic:

migrate:
	python3 manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi

start:
	python3 manage.py runserver

activate:
	. .venv/bin/activate