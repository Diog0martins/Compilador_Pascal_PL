#!/usr/bin/bash

for element in teste*.txt
do
  echo $element
  cat $element | python3 parserV1.py
done

