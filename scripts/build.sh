#!/bin/bash

rm -r build && git checkout build && echo "Build directory reset done" || exit 1
for dir in juniorguru/pages/*/
do
    dir=${dir%*/}  # remove the trailing '/'
    page=${dir##*/}  # everything after the final '/'
    python -m "juniorguru.pages.$page" && echo "Page $page done" || exit 1
done
npx rollup --config && echo "JavaScript done" || exit 1
