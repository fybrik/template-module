include Makefile.env

export DOCKER_TAG ?= 0.0.0
export DOCKER_USERNAME ?= fybrik
export DOCKER_PASSWORD ?= 
export DOCKER_HOSTNAME ?= ghcr.io
export DOCKER_NAMESPACE ?= fybrik
export DOCKER_NAME ?= @{{module_name}}

IMG := ${DOCKER_HOSTNAME}/${DOCKER_NAMESPACE}/${DOCKER_NAME}:${DOCKER_TAG}

export HELM_EXPERIMENTAL_OCI=1

all: test build

.PHONY: test
test:
	pipenv run python -m unittest discover

.PHONY: build
build:
	pipenv lock -r > requirements.txt
	docker build -f build/Dockerfile . -t ${IMG}
	rm requirements.txt

.PHONY: docker-push
docker-push:
	docker push ${IMG}

.PHONY: push-to-kind
push-to-kind:
	kind load docker-image ${IMG}

include hack/make-rules/helm.mk
include hack/make-rules/tools.mk
