#!/bin/sh
virtualenv -p python3.4 env
. ./env/bin/activate
pip3 install -r requirements.txt
