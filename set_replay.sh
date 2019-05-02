#!/bin/bash

if [ "$1" != "" ]; then 
  echo "Removing old replay file"
  rm ./web/js/replay_file.js 
  echo "Copying in new replay file"
  cp $1 ./web/js/replay_file.js 
else 
  echo "Expecting argument: filepath for replay file to be used"
fi
