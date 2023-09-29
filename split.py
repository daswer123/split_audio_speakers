import argparse
import json
import multiprocessing
from pydub import AudioSegment
from functools import partial
import whisperx
import torch
import gc 
import os

def process_speaker(data, speaker, pause_length):
    # Получаем расширение файла
    _, file_extension = os.path.splitext(data['audio_path'])
    # Удаляем точку перед расширением для использования в экспорте
    format_extension = file_extension.strip('.')
    
    # Загружаем аудио данные
    audio = AudioSegment.from_file(data['audio_path'], format=format_extension)
    
    # Создаем тихий аудиосегмент для паузы
    pause = AudioSegment.silent(duration=pause_length)

    # Создаем пустой аудиосегмент для говорящего
    speaker_audio = AudioSegment.empty()

    previous_speaker = None
    for segment in data['segments']:
        if 'speaker' in segment and segment['speaker'] == speaker:
            current_speaker = segment['speaker']
            start_time = int(segment['start'] * 1000)
            end_time = int(segment['end'] * 1000)
            if previous_speaker == current_speaker:
                speaker_audio += audio[start_time:end_time]
            else:
                speaker_audio += pause + audio[start_time:end_time]
            previous_speaker = current_speaker

    speaker_audio.export(f'{data["output_path"]}/{speaker}.mp3', format='mp3')
    # Сохраняем новый аудиофайл в его исходном формате
    # speaker_audio.export(f'{data["output_path"]}/{speaker}{file_extension}', format=format_extension)

def run_whisper(audio_file, output_path, pause_length,hf_token):
    device = "cuda" 
    batch_size = 16 
    compute_type = "float16"

    model = whisperx.load_model("large-v2", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size, language="ru")

    gc.collect(); torch.cuda.empty_cache(); del model

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    gc.collect(); torch.cuda.empty_cache(); del model_a

    diarize_model = whisperx.DiarizationPipeline(use_auth_token=hf_token, device=device)
    diarize_segments = diarize_model(audio)
    result = whisperx.assign_word_speakers(diarize_segments, result)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    with open(f'{output_path}/ready.json', 'w') as f:
        json.dump(result, f)

    data = {
        'audio_path': audio_file,
        'output_path': output_path,
        'segments': result['segments']
    }

    speakers = set(segment['speaker'] for segment in data['segments'] if 'speaker' in segment)
    with multiprocessing.Pool() as pool:
        pool.map(partial(process_speaker, data, pause_length=pause_length), speakers)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Обработка аудиофайла.')
    parser.add_argument('audio_file', type=str, help='Путь к аудиофайлу')
    parser.add_argument('output_path', type=str, help='Папка для вывода результатов')
    parser.add_argument('hf_token', type=str, help='Ваш токен на HF')
    parser.add_argument('--pause', type=int, default=300, help='Длина паузы в миллисекундах')
    args = parser.parse_args()

    run_whisper(args.audio_file, args.output_path, args.pause, args.hf_token)