#!/bin/bash
cd /config/mnt/rl_demo/model_cut/
for filename in *.stl; do
./binvox -e -d 64 "$filename"
done

