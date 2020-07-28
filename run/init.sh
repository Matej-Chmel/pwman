#!/bin/bash

echo Initializing git hooks.

# Move into root directory of this repository.
cd $(dirname "$(readlink -f "$0")")/..

git config core.hooksPath .hooks

if [[ $? == 0 ]]; then
    echo Hooks were configured successfully.
else
    echo Something went wrong.
    exit 1
fi

if [[ $OSTYPE != linux* ]]; then
    exit 0
fi

cd .hooks

# Grant x permission to each file without extension.
for file in *; do
    case $file in *.*) continue;; esac
    chmod +x $file
    echo Permission granted to $file.
done

if [[ $? == 0 ]]; then
    echo Permissions were granted to all hooks successfully.
else
    echo Something went wrong.
    exit 1
fi
