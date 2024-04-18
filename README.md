Данный сервис использует dockovpn для поднятия OpenVPN сервера в докер контейнере
Manager нужен для того, чтобы управлять ключами через API
Пример .env

````
HOST_ADDR=127.0.0.1
AUTH_KEY=test
COMMON_PATH=./dockovpn/config
KEY_PATH=./crt
OVPN_PATH=./vpn
CCD_PATH=./ccd
VPN_PORT=1180
API_PORT=5001
DEBUG=0
````
````
make prod
make copykey
make rebuild
````