import subprocess
import os
import time

# НАСТРОЙКИ
INPUT_STREAM = "https://stream8.cinerama.uz/1263/tracks-v1a1/mono.m3u8"
LOGO_URL = "https://i.postimg.cc/nrtrd8t7/Gemini-Generated-Image-hf4jb6hf4jb6hf4j.jpg"

def start_reencode():
    # Создаем папку dash вместо hls
    if not os.path.exists('dash'):
        os.makedirs('dash')

    ffmpeg_cmd = [
        'ffmpeg',
        '-re', 
        '-i', INPUT_STREAM,
        '-i', LOGO_URL,
        '-filter_complex', 
        # Увеличиваем лого до 280px
        '[1:v]scale=280:-1[logo];'
        '[0:v]fps=60,scale=1280:720[bg];'
        # ЛОГО ВЫШЕ: 15px от правого края и 15px от верхнего края
        '[bg][logo]overlay=main_w-overlay_w-15:15',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-b:v', '4500k',
        '-maxrate', '5000k',
        '-bufsize', '8000k',
        '-pix_fmt', 'yuv420p',
        '-g', '120',             # Ключевой кадр каждые 2 секунды (при 60fps)
        '-keyint_min', '120',
        '-sc_threshold', '0',    # Отключаем адаптивные ключи для стабильности DASH
        '-c:a', 'aac',
        '-b:a', '128k',
        # НАСТРОЙКИ DASH (.mpd)
        '-f', 'dash',
        '-seg_duration', '4',    # Длительность сегмента в секундах
        '-window_size', '6',     # Сколько сегментов держать в манифесте
        '-extra_window_size', '2',
        '-remove_at_exit', '1',  # Удалять файлы после завершения
        '-use_timeline', '1',
        '-use_template', '1',
        '-index_correction', '1',
        'dash/live.mpd'
    ]

    print("Запуск DASH-стрима WHATISFOOT.TV (720p 60fps)...")
    process = subprocess.Popen(ffmpeg_cmd)
    
    # 3 часа = 10800 секунд. Для тестов оставлю 900 (15 мин), поменяй под себя.
    time.sleep(10800) 
    process.terminate()

if __name__ == "__main__":
    start_reencode()
