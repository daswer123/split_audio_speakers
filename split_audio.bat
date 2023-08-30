@echo off

:: change path for your
set "AUDIO_PATH=audio.mp3"
set "OUTPUT_FOLDER=output"
set "DELAY_MS=300"


call venv/scripts/activate
python .\split.py %AUDIO_PATH%" %OUTPUT_FOLDER% --pause %DELAY_MS%