#/bin/bash

rm -rf dist/
uv build
uvx twine upload dist/*
