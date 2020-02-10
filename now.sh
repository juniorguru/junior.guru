#!/bin/bash
set -e

# Installation
npm install

pip install pipenv
curl https://pyenv.run | bash
source ~/.bashrc
pyenv install 3.7.5
pipenv install --dev --python="$(pyenv prefix 3.7.5)/bin/python"

# Build
pipenv run fetch  # needs $GOOGLE_SERVICE_ACCOUNT
pipenv run build
