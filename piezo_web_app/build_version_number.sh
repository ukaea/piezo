#!/usr/bin/env bash

version="__version__ = '`eval git describe --tags --long`'"
echo "$version" > PiezoWebApp/version.py
