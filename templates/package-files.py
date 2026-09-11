#!/usr/bin/env python3
"""Package verified HTML/PDF editions for an immutable GitHub release."""
import argparse,hashlib,json,shutil,zipfile
from pathlib import Path
from build import ROOT,build
TAG='templates-v3.0.0'
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
slugs=json.loads((ROOT/'review-set.json').read_text())['slugs'];files={}
package=args.output/'release';package.mkdir(exist_ok=True)
for slug in slugs:
 files[slug]={}
 for ext in ('html','pdf'):
  source=args.output/f'{slug}.{ext}';payload=source.read_bytes()
  if ext=='html':assert payload==build(slug),f'Stale HTML: {slug}'
  else:assert payload.startswith(b'%PDF-'),f'Invalid PDF: {slug}'
  files[slug][ext]={'url':f'https://github.com/clawdotme/plugin/releases/download/{TAG}/{slug}.{ext}','sha256':hashlib.sha256(payload).hexdigest(),'bytes':len(payload)}
  shutil.copyfile(source,package/source.name)
manifest={'schemaVersion':1,'releaseTag':TAG,'files':files}
(ROOT/'file-editions.json').write_text(json.dumps(manifest,indent=2)+'\n')
shutil.copyfile(ROOT/'file-editions.json',package/'file-editions.json')
with zipfile.ZipFile(package/'claw-me-100-templates.zip','w',zipfile.ZIP_DEFLATED) as z:
 for slug in slugs:
  for ext in ('html','pdf'):z.write(package/f'{slug}.{ext}',f'{slug}/{slug}.{ext}')
 z.write(package/'file-editions.json','file-editions.json')
print('Packaged 100 HTML and 100 PDF editions with checksums')
