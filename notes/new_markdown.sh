#!/bin/zsh

filename="${HOME}/Notes/$(date +"%Y%m%d_%H%M").md" 
 
touch $filename 
gnome-terminal --wait -- gvim -vc 'startinsert' $filename
 

if [ ! -s $filename ]; then
  rm $filename
else
  echo "FILENAME: $filename"
  firstline="$(head -n 1 $filename)"
  echo $firstline

  if [[ "$firstline" =~ "# " ]]; then
    new_filename="${${${firstline// /_}//\#/}:1}"
    mv "$filename" "$HOME}/Notes/${new_filename}.md"
 fi
fi
