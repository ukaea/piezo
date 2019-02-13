#!/usr/bin/env bash

echo "======================"
echo "Running flake8 ..."
flake8 PiezoWebApp

echo 
echo "======================"
echo "Running pylint ..."
pylint PiezoWebApp
