#!/usr/bin/env sh
# https://www.apache.org/licenses/LICENSE-2.0.html

set -e # Any command which returns non-zero exit code will cause this shell script to exit immediately
set -x # Activate debugging to show execution details: all commands will be printed before execution

python3 battleBadgesModifier.py

cd target/gui/flash/atlases
convert battleAtlas.png battleAtlas.dds
rm battleAtlas.png
cd -

python2 build.py
