#!/bin/zsh

dir=${HOME}/Notes

filename=$(ls -tR $dir | grep .md | head -n 1)
echo "Latest File: $filename"
 
gnome-terminal --wait -- gvim "$dir"


firstline=$(head -n 1 "$dir/$filename")
if [[ "$firstline" =~ "# " ]]; then
  new_filename="${${${firstline// /_}//\#/}:1}"
  mv "$dir/$filename" "$dir/${new_filename}.md"
fi


