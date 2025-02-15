import yt_dlp
import os
def download_youtube_video(url, output_path='.'):
    os.makedirs(output_path, exist_ok=True)
    ydl_opts = {
        # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': False
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download completed successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

video_url = "https://www.youtube.com/watch?v=wGGjVP5MB4k&list=PLU0Ir_rHTlbASLn01AIDlotVD9E0Roj2P"
download_youtube_video(video_url, output_path="data/khoa-hoc-alden-nguyen")