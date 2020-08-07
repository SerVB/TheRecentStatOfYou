#!/usr/bin/env sh
# https://www.apache.org/licenses/LICENSE-2.0.html

python3 battleBadgesModifier.py

cd target/gui/flash/atlases
convert battleAtlas.png battleAtlas.dds
rm battleAtlas.png
cd -

python2 build.py
