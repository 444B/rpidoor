#!/bin/bash
# this script assumes you are running it within the cloned repository
python3 -m venv .venv
source .venv/bin/activate
python3 install -r requirements.txt
nohup python3 door.py