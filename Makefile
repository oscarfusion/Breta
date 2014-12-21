TESTS=

run:
	python manage.py runserver

check_dependencies:
	pip list --outdated

lint_python:
	prospector

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

bootstrap:
	pip install -r requirements-dev.txt
	python manage.py syncdb
	python manage.py cities_light

test:
	python manage.py test $(TESTS) --failfast --settings=breta.test_settings
