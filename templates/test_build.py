import hashlib
import json
import unittest

from build import ROOT, SourceCheck, build


class TemplateBuildTests(unittest.TestCase):
    def test_every_template_is_reproducible_and_self_contained(self):
        for entry in json.loads((ROOT / 'catalog.json').read_text()):
            with self.subTest(slug=entry['slug']):
                payload = build(entry['slug'])
                self.assertEqual(hashlib.sha256(payload).digest(), hashlib.sha256(build(entry['slug'])).digest())
                self.assertIn(b'data:image/png;base64,', payload)
                self.assertIn(b'data:font/ttf;base64,', payload)
                self.assertIn(b'MIT License', payload)
                self.assertIn(b'SIL OPEN FONT LICENSE', payload)
                self.assertNotIn(b'../_shared/', payload)

    def test_rejects_active_markup_and_remote_images(self):
        for markup in ['<script>alert(1)</script>', '<img src="https://example.com/pixel.png">', '<img src="../_shared/studio.png" onerror="alert(1)">', '<iframe src="https://example.com">', '<svg/>']:
            with self.subTest(markup=markup), self.assertRaises(AssertionError):
                SourceCheck().feed(markup)

    def test_rejects_path_traversal(self):
        with self.assertRaises(AssertionError):
            build('../../private')


if __name__ == '__main__':
    unittest.main()
