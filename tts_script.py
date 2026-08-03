from gtts import gTTS
from pydub import AudioSegment

def tts_function(text, video_name):
    tts = gTTS(text=text, lang="en", slow=False, tld="co.uk")
    tts.save(video_name)
    print("Audio saved successfully!")
    audio = AudioSegment.from_mp3(video_name)
    faster_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 1.5)
    }).set_frame_rate(audio.frame_rate)
    faster_audio.export(video_name, format='mp3')
    print("speed increased")
    pass

def get_duration(video_path):
    audio = AudioSegment.from_mp3(video_path)
    duration_in_seconds = len(audio) / 1000.0
    print(duration_in_seconds)
    return duration_in_seconds