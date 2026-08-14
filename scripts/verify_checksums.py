#!/usr/bin/env python3
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
manifest=ROOT/'provenance'/'FILES.sha256'
fail=[]
for line in manifest.read_text().splitlines():
    if not line.strip(): continue
    expected,rel=line.split('  ',1)
    p=ROOT/rel
    h=hashlib.sha256(p.read_bytes()).hexdigest()
    if h!=expected: fail.append((rel,expected,h))
if fail:
    for x in fail: print('FAIL',*x)
    raise SystemExit(1)
print(f'PASS: {len(manifest.read_text().splitlines())} curated files match SHA-256 manifest.')
