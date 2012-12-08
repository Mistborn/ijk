#!/bin/bash

cat scripts/resetdb.sql | mysql -uroot -p
python manage.py syncdb
python scripts/fixdb.py