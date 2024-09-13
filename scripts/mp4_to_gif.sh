#!/bin/bash

# take input mp4 file
INPUT_MP4=$1
# output is just INPUT_MP4 name with .gif extension
OUTPUT_GIF="${INPUT_MP4%.*}.gif"
ffmpeg -i $INPUT_MP4 -vf "fps=10,scale=640:-1:flags=lanczos,palettegen" palette.png
ffmpeg -i $INPUT_MP4 -i palette.png -filter_complex "fps=10,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse" "$OUTPUT_GIF"