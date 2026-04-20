import subprocess
import os
import time

# НАСТРОЙКИ
INPUT_STREAM = "https://stream8.cinerama.uz/1263/tracks-v1a1/mono.m3u8"
LOGO_URL = "https://i.postimg.cc/nrtrd8t7/Gemini-Generated-Image-hf4jb6hf4jb6hf4j.jpg"

def start_reencode():
    if not os.path.exists('hls'):
        os.makedirs('hls')

    ffmpeg_cmd = [
        'ffmpeg',
        '-re', 
        '-i', INPUT_STREAM,
        '-i', LOGO_URL,
        '-filter_complex', 
        # Увеличиваем твое лого до 280px и разгоняем поток до 60 кадров
        '[1:v]scale=280:-1[logo];'
        '[0:v]fps=60,scale=1280:720[bg];'
        # Накладываем лого: 15px от правого края, 85px от верхнего (закрываем Сетанту)
        '[bg][logo]overlay=main_w-overlay_w-15:85',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-b:v', '4500k',        # Высокий битрейт для качества
        '-maxrate', '5000k',
        '-bufsize', '8000k',
        '-pix_fmt', 'yuv420p',
        '-g', '120',            # Интервал ключевых кадров
        '-c:a', 'aac',
        '-b:a', '128k',
        '-f', 'hls',
        '-hls_time', '4',
        '-hls_list_size', '6',
        '-hls_flags', 'delete_segments',
        '-hls_segment_filename', 'hls/seg_%d.ts',
        'hls/live.m3u8'
    ]

    print("Запуск WHATISFOOT.TV (720p 60fps)...")
    process = subprocess.Popen(ffmpeg_cmd)
    
    # Работаем 15 минут, затем деплоим (чтобы Action сохранился)
    # Для постоянного стрима нужно запускать на VPS
    time.sleep(900) 
    process.terminate()

if __name__ == "__main__":
    start_reencode()
