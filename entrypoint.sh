#!/bin/bash
flask db migrate
flask db upgrade
gunicorn --worker-class eventlet -w 1 --bin 0.0.0.0:80 wsgi:app --capture-output --log-level debug

