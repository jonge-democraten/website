#!/bin/sh

python website/manage.py dumpdata --all --natural-foreign --indent 2 forms pages sites blog auth.User auth.Group jdpages conf janeus events > website/fixtures/demo_data.json 
