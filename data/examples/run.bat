@echo off
set script_dir=%~dp0
set script_dir=%script_dir:~0, -1%
cd %script_dir%\..\..
cmd py -m src.main %*
