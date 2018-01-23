#!/bin/bash
gunicorn -b 0.0.0.0:8000 --workers=4 django_boards.wsgi
