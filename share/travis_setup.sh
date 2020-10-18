#!/bin/bash
set -evx

mkdir ~/.xazabcore

# safety check
if [ ! -f ~/.xazabcore/.xazab.conf ]; then
  cp share/xazab.conf.example ~/.xazabcore/xazab.conf
fi
