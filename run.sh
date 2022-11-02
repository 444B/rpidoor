#!/bin/bash
# this script assumes you are running it within the cloned repository
apt update
apt install sqlite3 python3 -y
python3 -m venv .venv
source .venv/bin/activate
python3 install -r requirements.txt
nohup python3 door.py
