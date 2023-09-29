# split_audio_speakers
This is an add-on to whisperX that allows you to split all speakers into audio files that are automatically generated from the original audio.

# Before start
To use this script you need to get your Hugging Face access token that you can generate from [Here](https://huggingface.co/settings/tokens) after the `--hf_token` argument and accept the user agreement for the following model: [Segmentation](https://huggingface.co/pyannote/segmentation), [Speaker Diarization](https://huggingface.co/pyannote/speaker-diarization-3.0)


# How to 
1) Run `install.bat` and wait for installation
2) Change the variables in the split_audio.bat file and run it
3) Or open powershell/cmd and type `.venv/scripts/activate` and `python split.py audio.mp3 out_path hf_token`

# Limitations
1) It was found that **audio files longer than 2 hours could not be processed**
2) You need a file in `mp3` format to work
