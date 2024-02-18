#!/bin/bash
# usage: bash format.sh

set -e

BASE_PATH=$(dirname $0)

echo "✨ Running black..."
black $BASE_PATH

echo "✨ Running isort..."
isort $BASE_PATH

echo "Done!🥳"