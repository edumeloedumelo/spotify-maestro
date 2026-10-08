"""Download de correspondências do YouTube; não usa a API do Spotify.

Registra fontes e pendências. Similaridade e duração são filtros aproximados,
não uma garantia de identidade das gravações.
"""
import argparse
import csv
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from rapidfuzz.fuzz import token_set_ratio
from yt_dlp import YoutubeDL


def normalize(value):
    value = unicodedata.normalize('NFKD', value.lower())
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in value if not unicodedata.combining(c))).strip()


def options():
    return {'quiet': True, 'noprogress': True, 'socket_timeout': 20,
            'retries': 1, 'extractor_retries': 1, 'cachedir': False,
            'js_runtimes': {'deno': {'path': str(Path.home() / '.spotdl/deno')}}}


def run_track(track, output, excluded_ids=()):
    index, artist, title, duration = track
    prefix = f'{int(index):02d} - '
    existing = list(output.glob(prefix + '*.mp3'))
    if existing:
        print(f'{index}/60 já existe: {existing[0].name}', flush=True)
        return {'index': int(index), 'artist': artist, 'title': title,
                'status': 'existente', 'file': str(existing[0])}
    expected = int(duration.split(':')[0]) * 60 + int(duration.split(':')[1])
    print(f'{index}/60 buscando: {artist} — {title}', flush=True)
    try:
        with YoutubeDL({**options(), 'extract_flat': True}) as ydl:
            search = ydl.extract_info(f'ytsearch5:{artist} {title}', download=False)
        candidates = []
        for entry in search.get('entries', []):
            if not entry or not entry.get('duration') or entry.get('id') in excluded_ids:
                continue
            video_title = normalize(entry.get('title', ''))
            artist_context = video_title + ' ' + normalize(entry.get('uploader', '') or entry.get('channel', ''))
            title_score = token_set_ratio(normalize(title), video_title)
            artist_score = max(token_set_ratio(normalize(a), artist_context) for a in artist.split(','))
            delta = abs(entry['duration'] - expected)
            # Reject obvious alternate versions absent from the requested title.
            alternate = any(word in video_title.split() and word not in normalize(title).split()
                            for word in ('cover', 'karaoke', 'sped', 'slowed', 'live', 'remix'))
            if title_score >= 85 and artist_score >= 80 and delta <= max(15, expected * .07) and not alternate:
                candidates.append((title_score + artist_score - delta, entry))
        if not candidates:
            result = {'index': int(index), 'artist': artist, 'title': title,
                      'status': 'pendente', 'reason': 'Sem correspondência com título, artista e duração próximos',
                      'candidates': [{k: e.get(k) for k in ('id', 'title', 'duration', 'url')} for e in search.get('entries', []) if e]}
            print(f'{index}/60 pendente: versão não confirmada', flush=True)
            return result
        entry = max(candidates, key=lambda item: item[0])[1]
        url = 'https://www.youtube.com/watch?v=' + entry['id']
        command = [sys.executable, '-m', 'yt_dlp', '--ignore-config', '--no-playlist',
                   '--no-progress', '--socket-timeout', '20', '--retries', '1',
                   '--js-runtimes', 'deno:' + str(Path.home() / '.spotdl/deno'),
                   '--ffmpeg-location', '/opt/homebrew/bin', '-f', 'bestaudio[ext=m4a]/bestaudio', '-x', '--audio-format', 'mp3',
                   '--audio-quality', '0', '--embed-metadata', '--write-info-json',
                   '-P', str(output), '-o', prefix + '%(title)s [%(id)s].%(ext)s', url]
        done = subprocess.run(command, capture_output=True, text=True, timeout=300)
        files = list(output.glob(prefix + '*.mp3'))
        success = done.returncode == 0 and bool(files)
        print(f'{index}/60 ' + ('MP3 salvo' if success else 'falhou'), flush=True)
        return {'index': int(index), 'artist': artist, 'title': title, 'source': url,
                'status': 'baixado' if success else 'falhou',
                'file': str(files[0]) if files else None,
                'error': done.stderr[-2000:] if not success else None}
    except Exception as exc:
        print(f'{index}/60 falhou: {exc}', flush=True)
        return {'index': int(index), 'artist': artist, 'title': title, 'status': 'falhou', 'error': str(exc)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=60)
    parser.add_argument('--retry-failed', action='store_true')
    parser.add_argument('--output', type=Path, default=Path.home() / 'Music/nova 1')
    args = parser.parse_args()
    with Path(__file__).with_name('nova-1.tsv').open(encoding='utf-8') as file:
        tracks = list(csv.reader(file, delimiter='\t'))[:args.limit]
    args.output.mkdir(parents=True, exist_ok=True)
    report = args.output / 'relatorio-download.json'
    results = json.loads(report.read_text(encoding='utf-8')) if report.exists() else []
    if args.retry_failed:
        failed = {str(item['index']) for item in results if item['status'] == 'falhou'}
        tracks = [track for track in tracks if track[0] in failed]
    with ThreadPoolExecutor(max_workers=2) as executor:
        for result in executor.map(lambda track: run_track(track, args.output), tracks):
            results = [item for item in results if item['index'] != result['index']] + [result]
            results.sort(key=lambda item: item['index'])
            report.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
    count = len(list(args.output.glob('*.mp3')))
    print(f'Concluído: {count} arquivos MP3 na pasta. Confira pendências em {report}', flush=True)


if __name__ == '__main__':
    main()
