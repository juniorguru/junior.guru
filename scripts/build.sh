#!/bin/bash

set -e
rm -r build && git checkout build && echo "Build directory reset done"
python -m juniorguru.index.build && echo "Page index done"
python -m juniorguru.jobs.build && echo "Page jobs done"
