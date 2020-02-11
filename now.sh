#!/bin/bash

# Get Python 3.7
if [[ ! -d ~/.pyenv ]]; then
  yum install -y libffi-devel sqlite-devel
  curl https://pyenv.run | bash
  export PATH="/$HOME/.pyenv/bin:$PATH"
fi

set -e
pyenv install 3.7.5 --skip-existing

# Installation
npm install
pip install pipenv
pipenv install --dev --python="$(pyenv prefix 3.7.5)/bin/python"

# Figure out things
env
ldd chrome | grep not

# Build
pipenv run fetch  # needs $GOOGLE_SERVICE_ACCOUNT
pipenv run build
