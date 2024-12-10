#!/bin/sh
pip3 install .
sphinx-build -E -c docs/ -b html docs/ result/