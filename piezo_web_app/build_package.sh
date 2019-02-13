#!/usr/bin/env bash

if [ -d ./dist ]; then
  echo "Removing existing dist folder"
  rm -rf ./dist
fi

python setup.py sdist bdist_wheel
