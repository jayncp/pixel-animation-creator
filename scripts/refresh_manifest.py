#!/usr/bin/env python3
"""Refresh content hashes for source and standalone skill; excludes Git metadata."""
import hashlib, pathlib, subprocess
root=pathlib.Path(__file__).resolve().parents[1]
paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z'],cwd=root).decode().split('\0')
files=sorted({p for p in paths if p and (root/p).is_file() and not (root/p).is_symlink()})
for folder, name in [(root,'CONTENT_MANIFEST.sha256'), (root/'skills/pixel-character-animation','MANIFEST.sha256')]:
    entries=[]
    for rel in files:
        p=root/rel
        if p.name in ('CONTENT_MANIFEST.sha256','MANIFEST.sha256') or not p.is_relative_to(folder): continue
        entries.append(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(folder).as_posix()}')
    (folder/name).write_text('\n'.join(entries)+'\n')
    print(folder/name)
