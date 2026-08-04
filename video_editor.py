import random
import whisper
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_audioclips, ImageClip
from moviepy.video.fx import Crop

def random_shorts_clip(video_path, output_path, clip_duration=35):
    clip = VideoFileClip(video_path)

    if clip.duration <= clip_duration:
        start_time = 0
    else:
        start_time = random.uniform(0, clip.duration - clip_duration)

    end_time = start_time + clip_duration

    short_clip = clip.subclipped(start_time, end_time)

    w, h = short_clip.size
    target_width = h * 9 / 16

    cropped_clip = short_clip.with_effects([
        Crop(width=target_width,
            height=short_clip.h,
            x_center=short_clip.w/2,
            y_center=short_clip.h/2)
    ])

    cropped_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac"
    )

    clip.close()
    short_clip.close()
    cropped_clip.close()

PIL_FONT = ImageFont.truetype(r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)

_dummy = Image.new("RGB", (1, 1))
_draw = ImageDraw.Draw(_dummy)

def wrap_text_center(text, max_width):
    """
    Wrap text by pixel width without breaking words.
    Every line will later be centered by TextClip.
    """
    words = text.split()
    lines = []
    current = ""

    for word in words:
        candidate = word if current == "" else current + " " + word

        if _draw.textlength(candidate, font=PIL_FONT) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return "\n".join(lines)

def add_Caption(video_path, start_time, duration, output_str):
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing audio...")
    result = model.transcribe(video_path)

    video = VideoFileClip(video_path)

    end_limit = start_time + duration
    subtitles = []

    print("Generating captions...")
    print(f"Total segments: {len(result['segments'])}")


    for segment in result["segments"]:
        print(f"{segment['start']:.2f} -> {segment['end']:.2f} : {segment['text']}")
        seg_start = segment["start"]
        seg_end = segment["end"]
        if seg_end < start_time or seg_start > end_limit:
            continue

        clip_start = max(seg_start, start_time)
        clip_end = min(seg_end, end_limit)

        text = segment["text"].strip()

        wrapped_text = wrap_text_center(text, video.w - 80)

        text_clip = (
            TextClip(
                text=wrapped_text+"\n",
                font=r"/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                font_size=24,
                color="white",
                stroke_color="black",
                stroke_width=2,
                method="label",          # <-- use label instead of caption
                text_align="center",     # center each line
                horizontal_align="center",
                vertical_align="center",
                interline=10,
            )
            .with_start(clip_start)
            .with_duration(clip_end - clip_start)
            .with_position(("center", "center"))
        )

        subtitles.append(text_clip)

    print("Muxing video...")
    final_video = CompositeVideoClip([video] + subtitles)

    final_video.write_videofile(
        output_str,
        codec="libx264",
        audio_codec="aac",
    )

    print(f"Success! Video saved to {output_str}")

def audio_n_video(video_path, hook_path, story_path, output_path):

    video = VideoFileClip(video_path)
    hook_audio = AudioFileClip(hook_path)
    story_audio = AudioFileClip(story_path)
    full_audio = concatenate_audioclips([hook_audio, story_audio])


    final_video = video.with_audio(full_audio)

    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    video.close()
    hook_audio.close()
    story_audio.close()
    final_video.close()

def add_reddit_banner(video_path, image_path, duration, start_time):

    video = VideoFileClip(video_path)

    overlay = (
        ImageClip(image_path)
        .resized(width=int(video.w * 0.80)) 
        .with_duration(duration)
        .with_start(start_time)
        .with_position("center")
    )

    final_video = CompositeVideoClip([video, overlay])

    final_video.write_videofile(
        "caption_short.mp4",
        codec="libx264",
        audio_codec="aac"
    )



