#!/bin/bash
echo "start gunicorn"
gunicorn --timeout 600 -k gevent -w 4 manager:app -b 0.0.0.0:8050