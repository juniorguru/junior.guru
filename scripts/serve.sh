#!/bin/bash

set -e
cd build
python -m http.server 8000 --bind 127.0.0.1
