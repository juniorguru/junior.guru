#!/bin/bash
set -e

# Installation
npm install
pip install setuptools pipenv
pipenv install --dev --three

# Build
pipenv run fetch  # needs $GOOGLE_SERVICE_ACCOUNT
pipenv run build
