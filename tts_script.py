import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel
from pydub import AudioSegment

def tts_function(text, voice, video_name):
    model_name = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
    model = Qwen3TTSModel.from_pretrained(
        "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice",
        device_map="cpu",
        dtype=torch.bfloat16,
    )
    wavs, sr = model.generate_custom_voice(
        text=text,
        language="English",
        speaker=voice,
    )
    sf.write(video_name, wavs[0], sr)
    print("Audio saved successfully!")
    pass

def get_duration(video_path):
    audio = AudioSegment.from_mp3(video_path)
    duration_in_seconds = len(audio) / 1000.0
    print(duration_in_seconds)
    return duration_in_seconds
