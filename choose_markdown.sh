#!/bin/zsh

dir=${HOME}/Notes

filename=$(ls -tR $dir | grep .md | head -n 1)
echo "Latest File: $filename"
 
kitty vim "$dir"


firstline=$(head -n 1 "$dir/$filename")
if [[ "$firstline" =~ "# " ]]; then
  fileending="${${firstline// /_}//\#/}"
  mv "$dir/$filename" "$dir/${filename:0:13}${fileending}.md"
fi


