#!/bin/bash
cd /home/code_repo/Apihealth_Monitor
python -m venv virtual_venv
source virtual_venv/bin/activate
pip install -r requirements.txt
nohup python service_monitor.py >log.txt &
sleep 13
python service_monitor_client.py


