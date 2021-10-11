#!/bin/bash
cd ../plaso && git stash && git pull && cd ..
pip install -r requirements.txt
pip install -r plaso/requirements.txt
cd pipeline && cp plaso-switch_improved.sh ../plaso/config/docker/plaso-switch.sh
docker build --no-cache -t plaso:latest ../plaso/config/docker/
