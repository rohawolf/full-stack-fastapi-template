#! /usr/bin/env bash
set -e
set -x

python /app/app/pre_start.py

bash ./scripts/test.sh "$@"
