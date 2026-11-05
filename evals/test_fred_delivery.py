"""Testes locais sem rede para validação e proteção contra sobrescrita."""
import importlib.util
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

PATH = pathlib.Path(__file__).resolve().parents[1] / 'downloads/fred-again/deliver.py'
SPEC = importlib.util.spec_from_file_location('fred_deliver', PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.source = self.root / 'source'
        self.destination = self.root / 'destination'
        (self.source / 'audio').mkdir(parents=True)
        # A decodificação é responsabilidade do downloader; aqui testamos entrega.
        audio = self.source / 'audio' / '01 - exemplo.mp3'
        audio.write_bytes(b'fixture de arquivo validado pelo downloader')
        self.record = dict(index=1, name='Exemplo', status='validated', file=audio.name,
                           sha256=MODULE.sha(audio), bytes=audio.stat().st_size, duration=1.0)
        (self.source / 'manifest.json').write_text(json.dumps({'tracks': [{'index': 1, 'name': 'Exemplo'}]}))
        (self.source / 'relatorio.json').write_text(json.dumps([self.record]))
        (self.source / 'audio' / 'fred again.m3u8').write_text('#EXTM3U\n' + audio.name + '\n')
        self.tags = patch.object(MODULE, 'EasyID3', return_value={'title': ['Exemplo']})
        self.tags.start()
        self.addCleanup(self.tags.stop)

    def test_check_only_does_not_write(self):
        result = MODULE.deliver(self.source, self.destination, True)
        self.assertFalse(result['copied'])
        self.assertFalse(self.destination.exists())
        self.assertFalse((self.source / 'delivery-verification.json').exists())

    def test_copy_and_repeat_preserve_verified_files(self):
        for _ in range(2):
            result = MODULE.deliver(self.source, self.destination)
            self.assertTrue(result['source_and_destination_sha256_match'])
        self.assertEqual(MODULE.sha(self.destination / self.record['file']), self.record['sha256'])

    def test_conflict_prevents_any_copy(self):
        self.destination.mkdir()
        (self.destination / 'manifest.json').write_text('arquivo anterior')
        with self.assertRaises(FileExistsError):
            MODULE.deliver(self.source, self.destination)
        self.assertFalse((self.destination / self.record['file']).exists())
        self.assertEqual((self.destination / 'manifest.json').read_text(), 'arquivo anterior')

    def test_tampered_audio_is_rejected(self):
        (self.source / 'audio' / self.record['file']).write_bytes(b'alterado')
        with self.assertRaises(ValueError): MODULE.deliver(self.source, self.destination)
        self.assertFalse(self.destination.exists())

    def test_pending_track_blocks_delivery(self):
        self.record['status'] = 'pending'
        (self.source / 'relatorio.json').write_text(json.dumps([self.record]))
        with self.assertRaises(ValueError): MODULE.deliver(self.source, self.destination)
        self.assertFalse(self.destination.exists())


if __name__ == '__main__':
    unittest.main()
