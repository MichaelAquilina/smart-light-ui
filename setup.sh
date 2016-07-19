#! /bin/sh

if [ -n "$VIRTUAL_ENV" ]; then
  echo "Symlinking gi module to $VIRTUAL_ENV"
  ln -s "/usr/lib/python3/dist-packages/gi" "$VIRTUAL_ENV/lib/python3.5"
else
  echo "Not currently in a virtualenv! Change to a virtualenv and re-run this script"
fi
