#!/bin/sh
virtualenv -p python3 env
. ./env/bin/activate
export PIP_DOWNLOAD_CACHE=/tmp/pip_cache
pip3 install -r requirements.txt
