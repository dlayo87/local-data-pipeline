@echo off
rem Used by Windows Task Scheduler. Runs the pipeline and writes a log file.
cd /d "%~dp0"
call .venv\Scripts\activate
python orchestration\pipeline.py >> pipeline_log.txt 2>&1
