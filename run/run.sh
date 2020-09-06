#!/bin/bash

# Move into root directory of this repository.
cd $(dirname "$(readlink -f "$0")")/..

# Run pwman.
python -m src.main $@
