#!/bin/bash
FLASK_APP=app.py
FLASK_RUN_HOST=0.0.0.0
FLASK_PORT=5000

if [[ $DEBUG == 1 ]]; then
  echo 'RUN IN DEBUG MODE...'
  python3 debug.py
else
  echo 'RUN IN PROD MODE...'
  uwsgi --ini app.ini
fi
