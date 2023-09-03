# split_audio_speakers
This is an add-on to whisperX that allows you to split all speakers into audio files that are automatically generated from the original audio.

# Before start
To use this script you need to get your Hugging Face access token that you can generate from [Here](https://huggingface.co/settings/tokens) after the `--hf_token` argument and accept the user agreement for the following model: [Segmentation](https://huggingface.co/pyannote/segmentation) , [Voice Activity Detection (VAD)](https://huggingface.co/pyannote/voice-activity-detection) , [Speaker Diarization](https://huggingface.co/pyannote/speaker-diarization)


# How to 
1) Run `install.bat` and wait for installation
2) Change the variables in the split_audio.bat file and run it
3) Or open powershell/cmd and type `call venv/scripts/activate` and `python split.py audio.mp3 out_path hf_token`
