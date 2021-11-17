#!/bin/bash

filename="${HOME}/Notes/$(date +"%Y%m%d_%H%M").md" 

touch $filename 
apostrophe $filename

if [ ! -s $filename ]; then
  rm $filename
fi

firstline=$(head -n 1 $filename)
echo $firstline
if [[ "$firstline" =~ "# " ]]; then
echo ${firstline:1}
mv "$filename"
fi
