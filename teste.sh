#!/usr/bin/bash

for element in Programas_Teste/teste*.pas
do
  echo $element
  cat $element | python3 parserV1.py
done

