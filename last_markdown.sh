#!/bin/bash

dir=${HOME}/Notes

unset -v latest
for file in "$dir"/*; do
  [[ $file -nt $latest ]] && latest=$file
done

apostrophe $latest

