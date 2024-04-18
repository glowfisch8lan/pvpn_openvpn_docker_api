SHELL := /bin/bash

run:
	export DEBUG=0; \
	docker-compose up -d --build --force-recreate

debug:
	export DEBUG=1; \
	docker-compose up -d --build

status:
	make -f app/Makefile status

stop:
	make -f app/Makefile stop