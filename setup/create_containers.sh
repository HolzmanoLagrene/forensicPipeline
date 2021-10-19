#!/bin/bash
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Please use a virtual environment or else your system is going to be messed up..."
    exit
fi
if [[ $(basename $PWD) != "setup" ]]; then
    echo "Please start this script from within setup folder"
    exit
fi

echo "--------------------------- Cloning Plaso ---------------------------"
git clone https://github.com/log2timeline/plaso.git ../plaso
pip install --upgrade pip
pip install -r ../requirements.txt
cp DO_NOT_TOUCH_plaso-switch_improved.sh ../plaso/config/docker/plaso-switch.sh
echo "--------------------------- Building Docker Container for Plaso ---------------------------"
sudo docker build -t plaso:latest ../plaso/config/docker/
echo "--------------------------- Building Docker Container for Python Notebook ---------------------------"
sudo docker build  -t notebook:latest .
rm -rf ../plaso