import subprocess
import os
import time

# КОНФИГУРАЦИЯ
INPUT_STREAM = "http://45.145.32.13:20440/match_futbol_2_hd/index.m3u8?token=test"
LOGO_URL = "https://i.postimg.cc/nrtrd8t7/Gemini-Generated-Image-hf4jb6hf4jb6hf4j.jpg"

def start_reencode():
    if not os.path.exists('hls'):
        os.makedirs('hls')

    ffmpeg_cmd = [
        'ffmpeg',
        '-i', INPUT_STREAM,
        '-i', LOGO_URL,
        '-filter_complex',
        '[1:v]scale=120:-1[logo];'
        '[0:v]fps=60,scale=1280:720[bg];'
        '[bg][logo]overlay=main_w-overlay_w-20:20',
        '-c:v', 'libx264',
        '-preset', 'veryfast',
        '-b:v', '3500k',
        '-maxrate', '4000k',
        '-bufsize', '6000k',
        '-pix_fmt', 'yuv420p',
        '-g', '60', # Кейфрейм каждую секунду для быстрой загрузки
        '-c:a', 'aac',
        '-b:a', '128k',
        '-f', 'hls',
        '-hls_time', '4',           # Длина одного фрагмента (4 сек)
        '-hls_list_size', '10',      # Хранить только последние 10 фрагментов
        '-hls_flags', 'delete_segments', # Удалять старые фрагменты
        '-hls_segment_filename', 'hls/seg_%d.ts',
        'hls/live.m3u8'              # Итоговый файл
    ]

    print("Запуск перекодирования в M3U8...")
    # Запускаем процесс в фоне или ограничиваем по времени для теста
    process = subprocess.Popen(ffmpeg_cmd)
    
    # Даем поработать 10 минут (в Actions можно увеличить)
    time.sleep(600) 
    process.terminate()

if __name__ == "__main__":
    start_reencode()
