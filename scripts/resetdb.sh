#!/bin/bash

python manage.py dumpdata --indent=4 > data.txt

cat scripts/resetdb.sql | mysql -uroot -p
python manage.py syncdb
python scripts/fixdb.py
