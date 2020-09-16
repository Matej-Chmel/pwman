@echo off

rem Move into root directory of this repository.
set script_dir=%~dp0
set script_dir=%script_dir:~0, -1%
cd %script_dir%\..

rem Run pwman.
py -m src.main %*
