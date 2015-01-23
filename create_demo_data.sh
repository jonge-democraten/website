#!/bin/sh

python website/manage.py dumpdata --all --natural --indent 2 forms pages sites blog auth.User jdpages conf > website/fixtures/demo_data.json 
