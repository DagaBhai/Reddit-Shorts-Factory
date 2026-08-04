import yt_dlp

def download():
  url = "https://www.youtube.com/watch?v=u7kdVe8q5zs"
  
  ydl_opts = {
      "format": "bestvideo+bestaudio/best",
      "merge_output_format": "mp4",
      "outtmpl": "%(title)s.%(ext)s",  # Save using the video title
  }
  
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download([url])
