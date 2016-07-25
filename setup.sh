#! /bin/sh

if [ -n "$VIRTUAL_ENV" ]; then
  pip install -r requirements.txt
  echo "Symlinking gi module to $VIRTUAL_ENV"
  ln -s "/usr/lib/python2.7/dist-packages/gi" "$VIRTUAL_ENV/lib/python2.7"
else
  echo "Not currently in a virtualenv! Change to a virtualenv and re-run this script"
fi
