#! /bin/bash
gunicorn --name work_management --timeout "120" --log-level debug -b 0.0.0.0:2000 -w 4 wsgi:app
