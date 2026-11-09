@echo off
rem Runs any dbt command from the project folder, for example: run_dbt build
pushd "%~dp0transform"
dbt %* --profiles-dir .
popd