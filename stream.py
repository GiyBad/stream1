import subprocess
import os
import time

INPUT_STREAM = "http://188.225.31.197/bpk-tv/000004499/tve/index.m3u8"
LOGO_URL = "https://i.postimg.cc/nrtrd8t7/Gemini-Generated-Image-hf4jb6hf4jb6hf4j.jpg"

def start_reencode():
    if not os.path.exists('hls'):
        os.makedirs('hls')

    ffmpeg_cmd = [
        'ffmpeg',
        '-i', INPUT_STREAM,
        '-i', LOGO_URL,
        '-filter_complex', '[1:v]scale=120:-1[logo];[0:v]fps=60,scale=1280:720[bg];[bg][logo]overlay=main_w-overlay_w-20:20',
        '-c:v', 'libx264', '-preset', 'veryfast', '-b:v', '3500k',
        '-c:a', 'aac', '-b:a', '128k',
        '-f', 'hls', '-hls_time', '4', '-hls_list_size', '5', '-hls_flags', 'delete_segments',
        'hls/live.m3u8'
    ]

    process = subprocess.Popen(ffmpeg_cmd)
    print("Стримим 5 минут...")
    time.sleep(300) # Поработает 5 минут и выключится, чтобы файлы загрузились
    process.terminate()

if __name__ == "__main__":
    start_reencode()
