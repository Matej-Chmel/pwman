#!/bin/bash

echo Soft reset called...

# Move into root directory of this repository.
cd $(dirname "$(readlink -f "$0")")/..

# Remove latest unpushed commit.
git reset --soft HEAD~1

# Remove staged changes.
git reset HEAD -- .

if [[ $? == 0 ]]; then
    echo Soft reset completed.
else
    echo Something went wrong.
    exit 1
fi
