#!/bin/bash
pip install -r requirements.txt

/usr/bin/supervisord -c /etc/supervisor/supervisord.conf