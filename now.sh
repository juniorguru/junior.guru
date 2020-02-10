#!/bin/bash

# Get Python 3.7
if [[ ! -d ~/.pyenv ]]; then
  yum install libffi-devel pyenv
#   curl https://pyenv.run | bash
#   export PATH="/zeit/.pyenv/bin:$PATH"
fi

set -e
pyenv install 3.7.5 --skip-existing

# Installation
npm install
pip install pipenv
pipenv install --dev --python="$(pyenv prefix 3.7.5)/bin/python"

# Build
pipenv run fetch  # needs $GOOGLE_SERVICE_ACCOUNT
pipenv run build
