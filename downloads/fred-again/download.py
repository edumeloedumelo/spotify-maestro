import argparse, concurrent.futures, hashlib, json, pathlib, re, shutil, subprocess, sys, unicodedata
from yt_dlp import YoutubeDL
from rapidfuzz.fuzz import token_set_ratio
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, WXXX

ROOT = pathlib.Path(__file__).resolve().parent
MANIFEST = json.loads((ROOT / 'manifest.json').read_text())
AUDIO = ROOT / 'audio'
FFMPEG = shutil.which('ffmpeg')
FFPROBE = shutil.which('ffprobe')
DENO = shutil.which('deno') or str(pathlib.Path.home() / '.spotdl/deno')

class Quiet:
    def debug(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

BASE = dict(quiet=True, no_warnings=True, logger=Quiet(), noplaylist=True,
            retries=1, extractor_retries=1, socket_timeout=20,
            js_runtimes={'deno': {'path': DENO}})

def norm(s):
    s = ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def check(path, expected):
    p = subprocess.run([FFPROBE, '-v', 'error', '-show_entries',
        'format=duration,size:stream=codec_name', '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    d = json.loads(p.stdout)
    duration = float(d['format']['duration'])
    if not any(s.get('codec_name') == 'mp3' for s in d['streams']): raise ValueError('Codec inválido')
    if abs(duration - expected) > 6: raise ValueError(f'Duração divergente: {duration} versus {expected}')
    subprocess.run([FFMPEG, '-v', 'error', '-xerror', '-i', str(path),
        '-f', 'null', '-'], capture_output=True, check=True)
    return dict(duration=duration, bytes=path.stat().st_size, sha256=hashlib.sha256(path.read_bytes()).hexdigest())

def search(t):
    reviewed_path = ROOT / 'reviewed-sources.json'
    reviewed = json.loads(reviewed_path.read_text()) if reviewed_path.exists() else {}
    if str(t['index']) in reviewed:
        h = reviewed[str(t['index'])]
        return [h], [h]
    query = ' '.join(t['artists'][:3]) + ' ' + t['name']
    with YoutubeDL({**BASE, 'extract_flat': True}) as y:
        hits = y.extract_info('ytsearch5:' + query, download=False)['entries']
    candidates = []
    wanted = norm(re.sub(r'\(?feat\.[^)]*\)?', '', t['name'], flags=re.I))
    for h in hits:
        full = norm(h.get('title', '') + ' ' + h.get('channel', ''))
        if abs((h.get('duration') or 0) - t['duration_ms']/1000) > 6: continue
        if any(v in full and v not in norm(t['name']) for v in ['remix', 'sped up', 'slowed', 'cover', 'live at', 'extended']): continue
        if 'remix' in wanted:
            version = norm(t['name'].split(' - ')[-1] if ' - ' in t['name'] else t['name'].split('(')[-1])
            if token_set_ratio(version, full) < 92: continue
        title = token_set_ratio(wanted, full)
        artist = token_set_ratio(norm(t['artists'][0]), full)
        if title < 90 or artist < 85: continue
        channel = norm(h.get('channel', ''))
        score = title + artist + (15 if 'topic' in channel else 0) + (8 if channel == norm(t['artists'][0]) else 0)
        candidates.append((score, h))
    return [h for _, h in sorted(candidates, key=lambda x: x[0], reverse=True)], [dict(id=h.get('id'), title=h.get('title'), channel=h.get('channel'), duration=h.get('duration')) for h in hits]

def work(t):
    stem = re.sub(r'[/\\:*?"<>|]', '_', f"{t['index']:02d} - {t['artists'][0]} - {t['name']}")[:220]
    path = AUDIO / (stem + '.mp3')
    r = dict(index=t['index'], name=t['name'], status='pending', file=path.name)
    reviewed_path = ROOT / 'reviewed-sources.json'
    reviewed = json.loads(reviewed_path.read_text()) if reviewed_path.exists() else {}
    source_review = reviewed.get(str(t['index']), {})
    expected = t['duration_ms']/1000
    if 'verified_catalog_duration' in source_review:
        r['duration_note'] = source_review['review']
        r['spotify_duration'] = expected
        expected = source_review['verified_catalog_duration']
        r['validation_duration_reference'] = 'Official YouTube catalog, same artist/title/album'
    try:
        if path.exists():
            old = next((x for x in json.loads((ROOT/'relatorio.json').read_text()) if x['index']==t['index']), {}) if (ROOT/'relatorio.json').exists() else {}
            if not old.get('source'): raise ValueError('Arquivo existente sem fonte registrada; preservado para revisão.')
            if old.get('sha256') != hashlib.sha256(path.read_bytes()).hexdigest(): raise ValueError('Arquivo existente alterado; preservado para revisão.')
            return {**old, **r, **check(path, expected), 'status': 'validated', 'existing': True}
        candidates, hits = search(t)
        r['candidates'] = hits
        if not candidates:
            return {**r, 'reason': 'Nenhuma correspondência segura de título, artista, versão e duração.'}
        errors = []
        for h in candidates[:2]:
            url = h.get('url') or h.get('webpage_url')
            for fmt in ['bestaudio', 'bestaudio[ext=m4a]']:
                try:
                    with YoutubeDL({**BASE, 'format': fmt, 'outtmpl': str(AUDIO / (stem + '.%(ext)s')),
                        'ffmpeg_location': str(pathlib.Path(FFMPEG).parent),
                        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '0'}]}) as y:
                        y.download([url])
                    check(path, expected)
                    tags = EasyID3(str(path))
                    tags['title'] = t['name']; tags['artist'] = t['artists']; tags['album'] = t.get('album', '')
                    tags['tracknumber'] = f"{t['index']}/{len(MANIFEST['tracks'])}"
                    tags.save()
                    tags = ID3(str(path)); tags.add(WXXX(encoding=3, desc='Spotify', url=t['url'])); tags.add(WXXX(encoding=3, desc='Audio source', url=url)); tags.save()
                    return {**r, **check(path, expected), 'status': 'validated', 'source': url,
                        'source_title': h.get('title'), 'source_channel': h.get('channel'), 'source_format': fmt}
                except Exception as e:
                    errors.append(str(e)[:400])
                    if path.exists():
                        bad = ROOT / 'incompletos'; bad.mkdir(exist_ok=True)
                        import uuid
                        path.rename(bad / (path.stem + '-' + uuid.uuid4().hex[:8] + '.mp3'))
        r['reason'] = '\n'.join(errors)
    except Exception as e: r['reason'] = str(e)[:600]
    return r

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Baixa correspondências da lista fixa manifest.json e valida MP3.')
    parser.add_argument('indices', type=int, nargs='*', help='Posições específicas; padrão: todas')
    parser.add_argument('--workers', type=int, choices=range(1,5), default=3)
    args = parser.parse_args()
    if not FFMPEG or not FFPROBE: parser.error('Instale FFmpeg e deixe ffmpeg/ffprobe no PATH.')
    if not pathlib.Path(DENO).is_file(): parser.error('Instale Deno no PATH ou em ~/.spotdl/deno.')
    AUDIO.mkdir(exist_ok=True)
    rp = ROOT / 'relatorio.json'
    previous = {r['index']: r for r in json.loads(rp.read_text())} if rp.exists() else {}
    selected = set(args.indices) if args.indices else {t['index'] for t in MANIFEST['tracks']}
    if not selected.issubset({t['index'] for t in MANIFEST['tracks']}): parser.error('Índice fora do manifesto.')
    for i, old in list(previous.items()):
        if old.get('status') == 'validated':
            f = AUDIO / old['file']
            if not f.exists() or hashlib.sha256(f.read_bytes()).hexdigest() != old.get('sha256'):
                previous[i] = {**old, 'status': 'pending', 'reason': 'Arquivo ausente ou alterado; requer nova validação.'}
    tracks = [t for t in MANIFEST['tracks'] if t['index'] in selected and previous.get(t['index'], {}).get('status') != 'validated']
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, t) for t in tracks]
        for future in concurrent.futures.as_completed(futures):
            r = future.result(); previous[r['index']] = r
            results = sorted(previous.values(), key=lambda r: r['index'])
            rp.write_text(json.dumps(results, ensure_ascii=False, indent=2))
            print(json.dumps({'done': len(results), 'valid': sum(r['status']=='validated' for r in results), 'index': r['index'], 'name': r['name'], 'status': r['status'], 'reason': r.get('reason', '')[:200]}, ensure_ascii=False), flush=True)
    valid = [r for r in sorted(previous.values(), key=lambda r: r['index']) if r['status']=='validated']
    (AUDIO / 'fred again.m3u8').write_text('#EXTM3U\n' + '\n'.join(r['file'] for r in valid) + '\n')
    print(f'VALIDATED {len(valid)}/{len(MANIFEST["tracks"])}', flush=True)
