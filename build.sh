#!/bin/bash
set -o errexit

# Determinar el directorio base
if [ -d "hoja de vida" ]; then
    cd "hoja de vida"
    REQ_PATH="../requirements.txt"
else
    REQ_PATH="requirements.txt"
fi

pip install -r $REQ_PATH
