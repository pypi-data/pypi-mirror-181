# AOC
Tools to support in solving the advent of code puzzles (see https://adventofcode.com/)

Several Point related functions (including rotation, manhattan distance), iterating the adjacent points or fetching data in a smart way

# Deploy to PyPi
## Pre-Req
- set the new version in `setup.py` – note that files which already exist in PyPi are not uploaded (note the error message)
- Install setuptools, wheel and the twine package by running `venv/bin/python -m pip install --upgrade setuptools wheel twine` in jetbrains console

## Deploy
1. Build the dist into /dist folder by running 
   `python -m build`
2. Upload to PyPi by running 
   `python -m twine upload dist/*`
   with username `__token__` and the password (see keepass)
