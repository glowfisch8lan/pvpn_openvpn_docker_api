SHELL := /bin/bash


rebuild:
	export DEBUG=0; \
	./rebuild.sh

prod:
	export DEBUG=0; \
	./deploy.sh

dev:
	export DEBUG=1; \
	./deploy.sh

key:
	openssl rand -hex 10

restart:
	docker restart ovpn_api
	docker restart ovpn_instance

copykey:
	docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/ca.crt  /opt/crt/ca.crt"
	docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/pvpn.key /opt/crt/server.key"
	docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/ca.key /opt/crt/ca.key"
	docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/pvpn.crt /opt/crt/server.crt"
	docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/dh.pem /opt/crt/dh.pem"
	docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/ta.key /opt/crt/ta.key"