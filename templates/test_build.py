import hashlib
import json
import re
import unittest

from build import ROOT, SourceCheck, build


class TemplateBuildTests(unittest.TestCase):
    def test_every_template_is_reproducible_and_self_contained(self):
        for entry in json.loads((ROOT / 'catalog.json').read_text()):
            with self.subTest(slug=entry['slug']):
                payload = build(entry['slug'])
                self.assertEqual(hashlib.sha256(payload).digest(), hashlib.sha256(build(entry['slug'])).digest())
                if '<img ' in (ROOT / entry['slug'] / 'index.html').read_text():
                    self.assertIn(b'data:image/png;base64,', payload)
                self.assertIn(b'data:font/ttf;base64,', payload)
                self.assertIn(b'MIT License', payload)
                self.assertIn(b'SIL OPEN FONT LICENSE', payload)
                self.assertNotIn(b'../_shared/', payload)

    def test_rejects_active_markup_and_remote_images(self):
        for markup in ['<script>alert(1)</script>', '<img src="https://example.com/pixel.png">', '<img src="../_shared/studio.png" onerror="alert(1)">', '<iframe src="https://example.com">', '<svg/>']:
            with self.subTest(markup=markup), self.assertRaises(AssertionError):
                SourceCheck().feed(markup)

    def test_each_template_has_distinct_hero_artwork(self):
        hashes = []
        for entry in json.loads((ROOT / 'catalog.json').read_text()):
            html = (ROOT / entry['slug'] / 'index.html').read_text()
            match = re.search(r'<img src="../_shared/([^"]+\.png)"', html)
            if match:
                hashes.append(hashlib.sha256((ROOT / '_shared' / match.group(1)).read_bytes()).hexdigest())
            self.assertLess(len(build(entry['slug'])), 8 * 1024 * 1024)
        self.assertEqual(len(hashes), len(set(hashes)))

    def test_template_navigation_targets_exist(self):
        for entry in json.loads((ROOT / 'catalog.json').read_text()):
            with self.subTest(slug=entry['slug']):
                html = (ROOT / entry['slug'] / 'index.html').read_text()
                targets = set(re.findall(r'id="([^"]+)"', html))
                links = set(re.findall(r'href="#([^"]+)"', html))
                self.assertFalse(links - targets, f"Missing sections: {links - targets}")

    def test_rejects_path_traversal(self):
        with self.assertRaises(AssertionError):
            build('../../private')


if __name__ == '__main__':
    unittest.main()
