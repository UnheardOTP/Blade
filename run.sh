#!/usr/bin/env bash
# BLADE Startup Script
set -e

PORT=

echo  ==========================================================
echo  Starting BLADE: The House of Severance on port ...
echo ==========================================================

if [  == --docker ] || [  == --docker ]; then
    echo Starting via Docker Compose...
    docker compose up --build -d
    echo 
 echo BLADE container is running in the background.
 echo Connect using: telnet localhost 2323 or nc localhost 2323
 echo To view logs: docker compose logs -f
 echo To stop: docker compose down
else
 python3 main.py --host 0.0.0.0 --port 
fi