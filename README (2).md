# Reddit Shorts Factory

Automatically generates Reddit-style story videos (YouTube Shorts / TikTok / Reels format) from start to finish — story writing, voiceover, Reddit-post banner, background clip, and burned-in captions — with a single script.

## How It Works

The pipeline in `main.py` runs through 9 steps:

1. **Generate a story** — Uses Gemini (`google-genai`) to write a short hook + story with a satisfying twist.
2. **Hook TTS** — Converts the hook text to speech.
3. **Story TTS** — Converts the story text to speech.
4. **Reddit banner** — Renders a fake Reddit post image containing the hook text.
5. **Duration calculation** — Measures the hook/story audio lengths to time the video.
6. **Background clip** — Grabs a random segment from a background video (e.g. gameplay/satisfying footage) matching the audio duration.
7. **Audio + video merge** — Combines the background clip with the hook/story audio.
8. **Banner overlay** — Overlays the Reddit post banner onto the video during the hook.
9. **Captions** — Transcribes the audio and burns in word-level captions, producing the final video.

Temporary files are cleaned up automatically, leaving only the final video.

## Project Structure

| File | Purpose |
|---|---|
| `main.py` | Orchestrates the full pipeline end to end |
| `script.py` | Generates the story hook + body using the Gemini API |
| `tts_script.py` | Text-to-speech generation and audio duration helpers |
| `hook_pic.py` | Creates the Reddit-style post banner image |
| `video_download.py` | Handles fetching/preparing background video footage |
| `video_editor.py` | Clips, merges audio/video, overlays the banner, and adds captions |

## Requirements

- Python 3.10+
- [FFmpeg](https://ffmpeg.org/) installed and available on your system PATH
- A Gemini API key
- A background video at `assets/background.mp4` (e.g. subway surfers/minecraft parkour style footage)

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/DagaBhai/Reddit-Shorts-Factory.git
   cd Reddit-Shorts-Factory
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API key:
   ```bash
   APIKEY=your_gemini_api_key_here
   ```

4. Add a background video at `assets/background.mp4`.

## Usage

Run the pipeline:

```bash
python main.py
```

The final video will be saved to `content/final_video.mp4`.

## Notes

- This project uses AI-generated stories and voices — review output before publishing.
- Make sure your background video is long enough to cover the generated audio duration; the script pulls a random segment sized to match it.

## License

No license specified — check with the repository owner before reuse.
