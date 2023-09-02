python -m venv venv
call venv/scripts/activate


pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install git+https://github.com/m-bain/whisperx.git
pip install pydub
