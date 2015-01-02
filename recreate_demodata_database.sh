#!/bin/sh

rm website/dev.db
python website/manage.py createdb --nodata --noinput
python website/manage.py loaddata demo_data
