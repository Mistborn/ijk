#!/bin/bash

python manage.py dumpdata --indent=4 --format=json alighi auth admin flatpages sites > data.json

