import json
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from baixar_nova_1 import run_track

output = Path.home() / 'Music/nova 1'
tracks = [
    ['21', 'Bruno Be', 'Walking On Water', '3:32'],
    ['42', 'meera', 'So Good meera Remix', '9:10'],
    ['59', 'Marshall Jefferson', 'Move Your Body Original Mix', '6:45'],
]
report = output / 'relatorio-download.json'
results = json.loads(report.read_text())
with ThreadPoolExecutor(max_workers=2) as executor:
    for result in executor.map(lambda track: run_track(track, output), tracks):
        old = next(item for item in results if item['index'] == result['index'])
        result['artist'], result['title'] = old['artist'], old['title']
        results = [item for item in results if item['index'] != result['index']] + [result]

url = 'https://www.youtube.com/watch?v=A317HI04sqY'
command = [sys.executable, '-m', 'yt_dlp', '--ignore-config', '--no-playlist',
           '--no-progress', '--socket-timeout', '20', '--retries', '1',
           '--js-runtimes', 'deno:' + str(Path.home() / '.spotdl/deno'),
           '--ffmpeg-location', '/opt/homebrew/bin', '-f', 'bestaudio[ext=m4a]/bestaudio',
           '-x', '--audio-format', 'mp3', '--audio-quality', '0', '--embed-metadata',
           '--write-info-json', '-P', str(output), '-o', '13 - %(title)s [%(id)s].%(ext)s', url]
done = subprocess.run(command, capture_output=True, text=True, timeout=300)
files = list(output.glob('13 - *.mp3'))
if done.returncode == 0 and files:
    item = next(item for item in results if item['index'] == 13)
    item.update(status='baixado', source=url, file=str(files[0]))
    item.pop('reason', None)
    print('13/60 MP3 salvo', flush=True)
else:
    print('13/60 falhou: ' + done.stderr[-1000:], flush=True)
results.sort(key=lambda item: item['index'])
report.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
