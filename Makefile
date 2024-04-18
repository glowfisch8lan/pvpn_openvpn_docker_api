SHELL := /bin/bash
export .env

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
	docker exec -ti ovpn_instance sh -c "cp /etc/openvpn/ca.crt  /opt/crt/ca.crt"
	docker exec -ti ovpn_instance sh -c "cp /etc/openvpn/pvpn.key /opt/crt/server.key"
	docker exec -ti ovpn_instance sh -c "cp /etc/openvpn/ca.key /opt/crt/ca.key"
	docker exec -ti ovpn_instance sh -c "cp /etc/openvpn/pvpn.crt /opt/crt/server.crt"
	docker exec -ti ovpn_instance sh -c "cp /etc/openvpn/dh.pem /opt/crt/dh.pem"
	docker exec -ti ovpn_instance sh -c "cp /etc/openvpn/ta.key /opt/crt/ta.key"