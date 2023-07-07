#!/usr/bin/env bash
export PORT=8089;

docker-compose up -d --build --force-recreate

docker-compose exec -ti ovpn_instance sh -c "cat /etc/openvpn/ca.crt > /opt/crt/ca.crt"
docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/PVPN.key /opt/crt/server.key"
docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/PVPN.crt /opt/crt/server.crt"
docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/dh.pem /opt/crt/dh.pem"
docker-compose exec -ti ovpn_instance sh -c "cp /etc/openvpn/ta.key /opt/crt/ta.key"
