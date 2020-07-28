echo Soft reset called...

rem Move into root directory of this repository.
set script_dir=%~dp0
set script_dir=%script_dir:~0, -1%
cd %script_dir%\..

rem Remove latest unpushed commit.
git reset --soft HEAD~1

rem Remove staged changes.
git reset HEAD -- .

if %errorlevel% == 0 (
    echo Soft reset completed.
) else echo Something went wrong.
