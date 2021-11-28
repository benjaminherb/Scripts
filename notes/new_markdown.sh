#!/bin/zsh

filename="${HOME}/Notes/$(date +"%Y%m%d_%H%M").md" 
 
touch $filename 
kitty vim -c 'startinsert' $filename
 

if [ ! -s $filename ]; then
  rm $filename
else
  echo "FILENAME: $filename"
  firstline="$(head -n 1 $filename)"
  echo $firstline

  if [[ "$firstline" =~ "# " ]]; then
    fileending="${${firstline// /_}//\#/}"
    mv "$filename" "${filename:0:-3}${fileending}.md"
 fi
fi
