#!/bin/bash

rm -r build && git checkout build && echo "Build directory reset done" || exit 1
python -m juniorguru.index.build && echo "Page index done" || exit 1
python -m juniorguru.learn.build && echo "Page learn done" || exit 1
python -m juniorguru.practice.build && echo "Page practice done" || exit 1
python -m juniorguru.jobs.build && echo "Page jobs done" || exit 1
python -m juniorguru.privacy.build && echo "Page privacy done" || exit 1
