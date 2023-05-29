#!/bin/bash

#This test checks if html generation from yaml is working

python yaml2html.py

cat ./html/czkawka.html

cat ./html/just.html

if ! cmp ./html/czkawka.html ./testfile1.html;then
    echo "test1 failed"
    exit 1
else
    echo "test1 passed"
fi

if cmp ./html/just.html ./testfile2.html;then
    echo "test2 failed"
    exit 1
else
    echo "test2 passed"
fi