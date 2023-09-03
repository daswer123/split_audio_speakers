@echo off

:: change path for your
set "AUDIO_PATH=audio.mp3"
set "OUTPUT_FOLDER=output"
set "HF_TOKEN=YOUR_TOKEN_HERE"

call venv/scripts/activate
python .\split.py "%AUDIO_PATH%" "%OUTPUT_FOLDER%" %HF_TOKEN%
pause