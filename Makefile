SHELL = /bin/sh +x
VIRTUALENV_NAME ?= UBER_TEST

# Each of your targets should be listed as .PHONY (unless you are actually
# compiling a C source file or similar)
# :r! grep '^[a-z-]\+:' % | cut -d: -f1 | sort
.PHONY: install test build virtualenv

install: virtualenv
	. ./bin/activate && sudo apt-get install couchdb && python ingestion.py

test:
	. ./bin/activate && nosetests  -sv ./app/test/

virtualenv:
	virtualenv --python=python2.7 --no-site-packages --setuptools --prompt="[$(VIRTUALENV_NAME)]" . && \
	. ./bin/activate && pip install -r requirements.txt
