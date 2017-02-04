#!/bin/bash
###############################################################################
# Initialize development environment.
# 
# This will run in the current virtualenv (or globally if none is active at
# the moment).
###############################################################################


function sysmsg() {
    echo -e "-- \e[32m$1\e[0m"
}
function infomsg() {
    echo -e "-- \e[1m$1\e[0m"
}


sysmsg "Initializing development environment"

infomsg "Updating pip and setuptools"
pip install -U pip setuptools

infomsg "Installing dependencies"
pip install -r requirements.txt

infomsg "Installing development dependencies"
pip install -r devrequirements.txt

infomsg "Running setup.py develop"
python setup.py develop
