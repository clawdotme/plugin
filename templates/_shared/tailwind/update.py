"""Install compiled Tailwind components without changing the existing brand CSS."""
import sys
from pathlib import Path
marker = '/* Generated Tailwind components */'
portal = Path(__file__).resolve().parents[1] / 'portal.css'
compiled = Path(sys.argv[1]).read_text()
portal.write_text(portal.read_text().split(marker)[0].rstrip() + '\n\n' + marker + '\n' + compiled)
