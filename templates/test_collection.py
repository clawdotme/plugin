import json
import unittest
from decimal import Decimal
from collection import ROOT, outputs

class CollectionTests(unittest.TestCase):
 def test_authored_editions_have_no_generated_drift(self):
  for name,content in outputs().items():
   with self.subTest(name=name):self.assertEqual((ROOT/name).read_text(),content)
 def test_financial_and_research_examples_reconcile(self):
  rows={x['slug']:x['rows'] for x in json.loads((ROOT/'collection.json').read_text())}
  for _,available,committed,free in rows['team-capacity-snapshot']:self.assertEqual(int(available),int(committed)+int(free))
  previous=None
  for _,opening,receipts,payments,closing in rows['cash-flow-snapshot']:
   self.assertEqual(int(opening)+int(receipts)-int(payments),int(closing))
   if previous is not None:self.assertEqual(int(opening),previous)
   previous=int(closing)
  for _,quantity,unit,total in rows['purchase-request']:self.assertEqual(Decimal(quantity)*Decimal(unit),Decimal(total))
  for _,base,seats,extra,total in rows['pricing-comparison']:self.assertEqual(int(base)+max(0,5-int(seats))*int(extra),int(total))
  for _,count,share in rows['survey-results']:self.assertEqual(int(count)/20*100,int(share[:-1]))
  self.assertEqual(sum(int(r[1]) for r in rows['survey-results']),20)
  self.assertEqual(sum(int(r[1]) for r in rows['travel-budget-worksheet']),900)
  self.assertEqual(sum(int(r[1]) for r in rows['expense-review']),760)
 def test_authored_content_is_distinct_and_sample_labeled(self):
  entries=json.loads((ROOT/'collection.json').read_text())
  self.assertEqual(len({e['headline'] for e in entries}),90)
  self.assertGreaterEqual(len({e['layout'] for e in entries}),18)
  for entry in entries:
   with self.subTest(slug=entry['slug']):
    from html import escape
    rendered = (ROOT / entry['slug'] / 'index.html').read_text()
    for section in entry['sections']:
     self.assertIn(escape(section['body']), rendered)
    self.assertGreaterEqual(len(entry['rows']),2)
    self.assertNotIn('Lorem ipsum',json.dumps(entry))
