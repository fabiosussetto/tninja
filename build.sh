#!/bin/bash

rm -rf build dist
python setup.py py2app -O2
python clean_build.py