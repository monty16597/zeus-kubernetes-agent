PIP_CMD ?= pip
VENV_DIR ?= .venv
DEPLOYMENT_DIR ?= ./deployment
DOCKER_REPO_URL ?= "manjeetalonjaekzero"
DOCKER_REPO_NAME ?= "pub"
DOCKER_REPO_IMAGE_TAG ?= "zeus-agent"

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
	make setup-venv3 && test ! -e requirements.txt || ($(VENV_RUN); $(PIP_CMD) -q install -r requirements.txt)

init:
	(make install-venv)

init3:
	(make install-venv3)

run:
	($(VENV_RUN); uvicorn app.main:app --host 0.0.0.0 --reload)

clean:
	(make uninstall; test -d $(VENV_DIR) && rm -r $(VENV_DIR))

deploy:
	kubectl apply -f $(DEPLOYMENT_DIR)/.

uninstall:
	kubectl delete -f $(DEPLOYMENT_DIR)/.

docker-build:
	docker build -t ${DOCKER_REPO_URL}/${DOCKER_REPO_NAME}:${DOCKER_REPO_IMAGE_TAG} .

docker-push:
	docker push ${DOCKER_REPO_URL}/${DOCKER_REPO_NAME}:${DOCKER_REPO_IMAGE_TAG}

docker-run:
	(docker rm -f zeus-agent || echo "No containers exist. deploying one..."; \
		docker run --name zeus-agent -p 8000:8000 -it ${DOCKER_REPO_URL}/${DOCKER_REPO_NAME}:${DOCKER_REPO_IMAGE_TAG}; \
		docker rm -f zeus-agent)
