#!/bin/bash

#This test checks if html generation from yaml is working

python yaml2html.py -d ./html/ czkawka.yml just.yml

if diff ./html/czkawka.html ./testfile1.html; then
    echo "test1 passed"
else
    echo "test1 failed"
    exit 1
fi

if diff ./html/just.html ./testfile2.html; then
    echo "test2 passed"
else
    echo "test2 failed"
    exit 1
fi