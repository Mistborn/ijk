#!/bin/bash

./manage.py dumpdata --indent=4 --format=json $1 > backups/data-$1.$(date --utc '+%Y-%m-%d').json

