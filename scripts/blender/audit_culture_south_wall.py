"""Run the established detailed south wall check without replacing the predecessor report."""
from pathlib import Path
import sys,runpy
ROOT=Path(__file__).resolve().parents[2];version=sys.argv[sys.argv.index('--')+1]
out=ROOT/'deliverables'/version;file=out/'preservation_validation.json';original=file.read_bytes()
try:
 runpy.run_path(str(Path(__file__).parent/'audit_preserved_south_gate.py'),run_name='__main__')
 (out/'south_gate_preservation_validation.json').write_bytes(file.read_bytes())
finally:file.write_bytes(original)
if version=='v0.0.42':
 runpy.run_path(str(Path(__file__).parent/'audit_south_registered_layout.py'),run_name='__main__')
