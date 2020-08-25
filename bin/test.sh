runr#!/usr/bin/env bash

# run in container
cd /opt/test/api
python -m unittest test_cloudservice_api.py
cd /opt