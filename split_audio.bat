@echo off

:: change path for your
set "AUDIO_PATH=out.wav"
set "OUTPUT_FOLDER=spongeBob"

call venv/scripts/activate
python .\split.py "%AUDIO_PATH%" "%OUTPUT_FOLDER%"
pause