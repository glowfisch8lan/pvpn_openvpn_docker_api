SHELL := /bin/bash
prod:
	export DEBUG=0; \
	./deploy.sh

dev:
	export DEBUG=1; \
	./deploy.sh

key:
	openssl rand -hex 40