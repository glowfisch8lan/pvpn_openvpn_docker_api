TODO:
1. Ротация логов

````
make build - сборка в PROD режиме
make build-debug - сборка в DEBUG режиме
make status - статус Supervisor сущности
make stop - остановить SUpervisor сущность
````

````
apt-get install build-essential
python -m pip install -r requirements.txt
set PYTHONUNBUFFERED=1;set FLASK_APP=app.py;set FLASK_ENV=production; python3 wsgi.py
````

Установка:
Заполнить .env