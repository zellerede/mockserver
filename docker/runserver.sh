#!/bin/bash

DIR=$(dirname "$0")

if [ -n "$HTTPS" ]
then
  $DIR/manage.py runsslserver 0.0.0.0:443
else
  $DIR/manage.py runserver 0.0.0.0:8000
fi

