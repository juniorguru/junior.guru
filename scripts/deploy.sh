#!/bin/bash

set -e
cd build

if [[ -n "$NOW_TOKEN" ]]; then
    now_token_option="--token=$NOW_TOKEN"
fi
if [[ -n "$NOW_TARGET" ]]; then
    now_target_option="--target=$NOW_TARGET"
fi
now --confirm --no-clipboard "$now_token_option" "$now_target_option"
