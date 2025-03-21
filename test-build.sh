#!/bin/sh
pip3 install .
sphinx-build -j auto -E -c docs/ -b html docs/ result/