import json
import re
import tempfile
import unittest
from pathlib import Path
from build import ROOT
from review import render


class ReviewSetTests(unittest.TestCase):
    def test_hundred_complete_pairs_cover_ten_categories(self):
        selected = json.loads((ROOT / 'review-set.json').read_text())['slugs']
        catalog = {x['slug']: x for x in json.loads((ROOT / 'catalog.json').read_text())}
        self.assertEqual(len(selected), 100)
        self.assertEqual(len(set(selected)), 100)
        self.assertEqual(len({catalog[s]['category'] for s in selected}), 10)
        from collections import Counter
        self.assertEqual(set(Counter(catalog[s]["category"] for s in selected).values()), {10})
        self.assertEqual(set(selected), set(catalog))
        prompts = []
        for slug in selected:
            with self.subTest(slug=slug):
                brief = json.loads((ROOT / slug / 'creation-brief.json').read_text())
                self.assertEqual(brief['slug'], slug)
                self.assertGreaterEqual(len(brief['exampleAnswers']), 5)
                self.assertTrue(brief['creationPromptOrigin'])
                self.assertIn('private', brief['customizationPrompt'])
                self.assertNotEqual(brief['creationPrompt'], brief['customizationPrompt'])
                prompts.extend([brief['creationPrompt'], brief['customizationPrompt']])
        self.assertEqual(len(set(prompts)), 200)

    def test_review_pages_link_to_both_prompts_and_the_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            render(output)
            slugs = json.loads((ROOT / 'review-set.json').read_text())['slugs']
            pages = [output / f'{slug}-review.html' for slug in slugs]
            self.assertEqual(len(pages), 100)
            for page in pages:
                content = page.read_text()
                self.assertIn('Start with this template', content)
                self.assertIn('Build your own version', content)
                self.assertIn('Example brief', content)
                for target in re.findall(r'(?:href|src)="([^"#]+\.html)"', content):
                    self.assertTrue((output / target).is_file(), target)

    def test_budget_rows_and_totals_reconcile(self):
        html = (ROOT / 'budget-overview/index.html').read_text()
        tbody = re.search(r'<tbody>(.*?)</tbody>', html, re.S).group(1)
        rows = [[int(value.replace(',', '')) for value in re.findall(r'<td>([\d,]+)</td>', row)] for row in re.findall(r'<tr>(.*?)</tr>', tbody)]
        self.assertEqual(len(rows), 4)
        for planned, actual, remaining in rows:
            self.assertEqual(planned - actual, remaining)
        totals = [sum(row[i] for row in rows) for i in range(3)]
        footer = re.search(r'<tfoot>(.*?)</tfoot>', html).group(1)
        self.assertEqual(totals, [int(value.replace(',', '')) for value in re.findall(r'<td>([\d,]+)</td>', footer)])
