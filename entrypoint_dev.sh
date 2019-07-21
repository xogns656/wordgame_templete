#!/bin/bash

set -e

# Run
case "$1" in
    start)
        echo "Running Development Server on 0.0.0.0:923"
        python minigame/manage.py runserver 0.0.0.0:923 --verbosity 3

esac