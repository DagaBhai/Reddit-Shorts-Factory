import os
import shutil
import json
from script import get_story
from tts_script import tts_function, get_duration
from hook_pic import create_rectangle_with_overlays
from video_download import download
from video_editor import random_shorts_clip, audio_n_video, add_reddit_banner, add_Caption

OUTPUT_DIR = "content"
if os.path.exists(OUTPUT_DIR):
    shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

HOOK_MP3 = os.path.join(OUTPUT_DIR, "hook.mp3")
STORY_MP3 = os.path.join(OUTPUT_DIR, "story.mp3")
BANNER = os.path.join(OUTPUT_DIR, "final_output.png")
SHORT_CLIP = os.path.join(OUTPUT_DIR, "shorts_output.mp4")
MERGED_VIDEO = os.path.join(OUTPUT_DIR, "new_story.mp4")
BANNER_VIDEO = os.path.join(OUTPUT_DIR, "caption_short.mp4")
FINAL_VIDEO = os.path.join(OUTPUT_DIR, "final_video.mp4")

print("[0/9] Downloading bg video...")
download()
print(" -> bg video Downloaded successfully loaded.")

print("[1/9] Loading story script...")
script = json.loads(get_story())
hook = script["hook"]
story = script["story"]
print(story)
print(" -> Story script successfully loaded.")

print("[2/9] Generating Hook TTS...")
tts_function(hook, video_name=HOOK_MP3)
print(" -> Hook audio generated.")

print("[3/9] Generating Story TTS...")
tts_function(story, video_name=STORY_MP3)
print(" -> Story audio generated.")

print("[4/9] Creating Reddit banner...")
create_rectangle_with_overlays(hook)
os.replace("final_output.png", BANNER)
print(" -> Banner created.")

print("[5/9] Calculating durations...")
hook_duration = get_duration(HOOK_MP3)
story_duration = get_duration(STORY_MP3)
total_duration = hook_duration + story_duration
print(
    f"Hook: {hook_duration:.2f}s | "
    f"Story: {story_duration:.2f}s | "
    f"Total: {total_duration:.2f}s"
)

print("[6/9] Creating background clip...")
random_shorts_clip(
    "short.mp4",
    SHORT_CLIP,
    clip_duration=total_duration,
)

print("[7/9] Merging audio/video...")
audio_n_video(
    SHORT_CLIP,
    HOOK_MP3,
    STORY_MP3,
    MERGED_VIDEO,
)

print("[8/9] Applying Reddit banner overlay...")
add_reddit_banner(
    MERGED_VIDEO,
    BANNER,
    hook_duration,
    0,
)
os.replace("caption_short.mp4", BANNER_VIDEO)


# 9. Burn-in Captions & Final Export
print("[9/9] Generating and adding captions to final video...")
add_Caption(
    BANNER_VIDEO,
    hook_duration,
    story_duration,
    FINAL_VIDEO,
)

print("Final video created!")

print("Cleaning temporary files...")

for file in [
    HOOK_MP3,
    STORY_MP3,
    BANNER,
    SHORT_CLIP,
    MERGED_VIDEO,
    BANNER_VIDEO,
]:
    if os.path.exists(file):
        os.remove(file)

print(f"Done!\nFinal video: {FINAL_VIDEO}")
