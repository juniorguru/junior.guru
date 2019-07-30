#!/bin/bash

set -e
rm -r build && git checkout build && echo "Build directory reset done"
python -m juniorguru.index.build && echo "Page index done"
python -m juniorguru.learn.build && echo "Page learn done"
python -m juniorguru.practice.build && echo "Page practice done"
python -m juniorguru.jobs.build && echo "Page jobs done"
python -m juniorguru.privacy.build && echo "Page privacy done"
