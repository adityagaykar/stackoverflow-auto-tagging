#!/bin/bash
# $1 = path to test title-tag.out file 
# $2 = path to train title-tag.out file
python ../py-src/sklearn_test.py $1 $2
