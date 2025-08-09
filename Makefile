install:
	uv install

collectstatic:

migrate:
	python3 manage.py migrate

build:
	./build.sh

render-start:
	gunicorn task_manager.wsgi
