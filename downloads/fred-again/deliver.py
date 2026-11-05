"""Confere o lote e copia arquivos validados, sem substituir destinos diferentes."""
import argparse
import hashlib
import json
import pathlib
import shutil
from mutagen.easyid3 import EasyID3


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def deliver(source, destination, check_only=False):
    manifest = json.loads((source / 'manifest.json').read_text())
    results = json.loads((source / 'relatorio.json').read_text())
    tracks = {t['index']: t for t in manifest['tracks']}
    if len(results) != len(tracks) or {r['index'] for r in results} != set(tracks):
        raise ValueError('Relatório incompleto ou com posições duplicadas.')
    results.sort(key=lambda r: r['index'])
    for r in results:
        if r['status'] != 'validated': raise ValueError(f"Faixa pendente: {r['name']}")
        if pathlib.Path(r['file']).name != r['file']: raise ValueError('Nome de arquivo inválido.')
        audio = source / 'audio' / r['file']
        if sha(audio) != r['sha256']: raise ValueError(f'Arquivo alterado: {audio.name}')
        if EasyID3(str(audio))['title'][0] != tracks[r['index']]['name']:
            raise ValueError(f'Metadados divergentes: {audio.name}')
    entries = [s for s in (source / 'audio' / 'fred again.m3u8').read_text().splitlines() if s and not s.startswith('#')]
    if entries != [r['file'] for r in results]: raise ValueError('Ordem da playlist divergente.')
    summary = {'audio_count': len(results), 'bytes': sum(r['bytes'] for r in results),
               'duration_seconds': sum(r['duration'] for r in results),
               'duration_exceptions': [{'name': r['name'], 'actual': r['duration'], 'spotify': r['spotify_duration']}
                                       for r in results if 'duration_note' in r]}
    if check_only:
        return {**summary, 'mode': 'check-only', 'copied': False}
    files = [(source / 'audio' / r['file'], r['file']) for r in results]
    files += [(source / 'audio' / 'fred again.m3u8', 'fred again.m3u8')]
    files += [(source / n, n) for n in ['manifest.json', 'relatorio.json']]
    # Verificar conflitos antes de copiar qualquer arquivo.
    for src, name in files:
        target = destination / name
        if target.exists() and sha(src) != sha(target):
            raise FileExistsError(f'Destino diferente preservado: {target}')
    destination.mkdir(parents=True, exist_ok=True)
    for src, name in files:
        target = destination / name
        if not target.exists():
            with src.open('rb') as inf, target.open('xb') as outf:
                shutil.copyfileobj(inf, outf)
        if sha(src) != sha(target): raise ValueError(f'Cópia divergente: {target}')
    summary.update(destination=str(destination), copied=True, source_and_destination_sha256_match=True)
    (source / 'delivery-verification.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent)
    parser.add_argument('--output', type=pathlib.Path, default=pathlib.Path.home() / 'Music' / 'fred again')
    parser.add_argument('--check-only', action='store_true', help='Valida sem copiar ou escrever arquivos')
    args = parser.parse_args()
    print(json.dumps(deliver(args.source, args.output, args.check_only), ensure_ascii=False, indent=2))
