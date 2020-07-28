rem Move into root directory of this repository.
set script_dir=%~dp0
set script_dir=%script_dir:~0, -1%
cd %script_dir%\..

echo Initializing git hooks.

git config core.hooksPath .hooks

if %errorlevel% == 0 (
    echo Hooks were configured successfully.
) else echo Something went wrong.
