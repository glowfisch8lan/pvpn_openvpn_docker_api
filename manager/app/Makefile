SHELL := /bin/bash

status:
	docker exec -ti  backend_vpn sh -c "supervisorctl status"

stop:
	docker exec -ti  backend_vpn sh -c "supervisorctl stop app-run:app-run_00 && pkill -f uwsgi -9"

debug:
	export DEBUG=1; \
	/app/start.sh