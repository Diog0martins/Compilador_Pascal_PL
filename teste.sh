#!/usr/bin/bash

for element in programas_teste/teste*.pas
do
  echo $element
  cat $element | python3 parserV1.py
done

