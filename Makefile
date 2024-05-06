help:
	@echo "Tasks in \033[1;32mdemo\033[0m:"
	@cat Makefile

lint:
	mypy src --ignore-missing-imports
	flake8 src --ignore=$(shell cat .flakeignore)

dev:
	pipenv run python setup.py develop

test: dev
	pytest

clean:
	@rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/
	
build: clean
	pipenv install --dev wheel
	pipenv run python setup.py bdist_wheel
stable:
	cp dist/at_config-*.*-py3-none-any.whl dist/at_config-stable-py3-none-any.whl
latest:
	cp dist/at_config-*.*-py3-none-any.whl dist/at_config-latest-py3-none-any.whl
incver:
	pipenv run python ./scripts/incver.py
requirements:
	pipenv run python -m pip freeze | sed '/^-e git/d' > requirements.txt
	pipenv run python ./scripts/fix_requirements.py
rabbit:
	docker run --rm -p 15672:15672 -p 5672:5672 rabbitmq:management