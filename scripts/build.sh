#!/bin/bash

set -e
rm -r build && git checkout build
python juniorguru/index/build.py
python juniorguru/jobs/build.py
