PIP_CMD ?= pip
VENV_DIR ?= .venv
DEPLOYMENT_DIR ?= ./deployment

ifeq ($(OS), Windows_NT)
	VENV_RUN = . $(VENV_DIR)/Scripts/activate
else
	VENV_RUN = . $(VENV_DIR)/bin/activate
endif

setup-venv:
	(test `which virtualenv` || $(PIP_CMD) install --user virtualenv) && \
		(test -e $(VENV_DIR) || python -m virtualenv $(VENV_DIR))

setup-venv3:
	(test `which virtualenv` || $(PIP_CMD) install --user virtualenv) && \
		(test -e $(VENV_DIR) || python3 -m virtualenv $(VENV_DIR))

install-venv:
	make setup-venv && test ! -e requirements.txt || ($(VENV_RUN); $(PIP_CMD) -q install -r requirements.txt)

install-venv3:
	make setup-venv-python3 && test ! -e requirements.txt || ($(VENV_RUN); $(PIP_CMD) -q install -r requirements.txt)

init:
	(make install-venv)

init3:
	(make install-venv3)

run:
	($(VENV_RUN); uvicorn main:app --reload)

clean:
	(make uninstall; test -d $(VENV_DIR) && rm -r $(VENV_DIR))

deploy:
	kubectl apply -f $(DEPLOYMENT_DIR)/.

uninstall:
	kubectl delete -f $(DEPLOYMENT_DIR)/.