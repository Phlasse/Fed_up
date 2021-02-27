# ----------------------------------
#          INSTALL & TEST
# ----------------------------------
install_requirements:
	@pip install -r requirements.txt

check_code:
	@flake8 scripts/* Fed_up/*.py

black:
	@black scripts/* Fed_up/*.py

test:
	@coverage run -m pytest tests/*.py
	@coverage report -m --omit=$(VIRTUAL_ENV)/lib/python*

ftest:
	@Write me

clean:
	@rm -f */version.txt
	@rm -f .coverage
	@rm -fr */__pycache__ */*.pyc __pycache__
	@rm -fr build dist
	@rm -fr Fed_up-*.dist-info
	@rm -fr Fed_up.egg-info

install:
	@pip install -e .

all: clean install test black check_code


uninstall:
	@python setup.py install --record files.txt
	@cat files.txt | xargs rm -rf
	@rm -f files.txt

count_lines:
	@find ./ -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./scripts -name '*-*' -exec  wc -l {} \; | sort -n| awk \
		        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''
	@find ./tests -name '*.py' -exec  wc -l {} \; | sort -n| awk \
        '{printf "%4s %s\n", $$1, $$2}{s+=$$0}END{print s}'
	@echo ''

# ----------------------------------
#      UPLOAD PACKAGE TO PYPI
# ----------------------------------
build:
	@python setup.py sdist bdist_wheel

pypi_test:
	@twine upload -r testpypi dist/* -u lologibus2

pypi:
	@twine upload dist/* -u lologibus2


# ----------------------------------
#      HEROKU - GOOGLE CREDENTIALS
# ----------------------------------

heroku_set_gcp_env:
	-@heroku config:set GOOGLE_APPLICATION_CREDENTIALS="$(< /home/olivier/.gcp/Fed-Up-0d6d83f73bd5.json)"
