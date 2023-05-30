#!/bin/bash

#This test checks if html generation from yaml is working

python yaml2html.py

if ! cmp -s ./html/czkawka.html ./testfile1.html;then
    echo "test1 failed"
    exit 1
else
    echo "test1 passed"
fi

if cmp -s ./html/just.html ./testfile2.html;then
    echo "test2 failed"
    exit 1
else
    echo "test2 passed"
fi