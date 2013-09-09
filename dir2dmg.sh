#!/bin/bash

if [ "$#" -eq 0 ]; then
  echo "Usage:"
  echo "   dir2dmg <path/to/directory>"
  exit 1
fi

PWD=`pwd`

function dmg() {
  dir="$1"
  if [ ! -d "$dir" ]; then
    echo "$dir is not a directory!"
    exit 1
  fi
  if [ ! -r "$dir" ]; then
    echo "$dir is not readable!"
    exit 1
  fi
  vol=$( basename "$dir" )
  echo "hdiutil create -volname \"$vol\" -srcfolder \"$dir\" -format UDZO \"$PWD/$vol\""
  hdiutil create -volname "$vol" -srcfolder "$dir" -format UDZO "$PWD/$vol"
}

while [[ $# > 0 ]]; do
  dmg "$1"
  shift
done