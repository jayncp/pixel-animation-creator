#!/usr/bin/env python3
"""Validate release structure and local links. Does not certify artwork."""
import argparse, hashlib, json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/pixel-character-animation'

def validate():
    failures = []
    required = ['SKILL.md', 'agents/openai.yaml', 'scripts/pixel_anim.py', 'scripts/project_stage.py', 'references/project-spec.md']
    for p in required:
        if not (SKILL / p).is_file(): failures.append(f'missing {p}')
    body = (SKILL / 'SKILL.md').read_text()
    if not body.startswith('---\n') or 'name: pixel-character-animation' not in body.split('---')[1]:
        failures.append('invalid skill frontmatter')
    for p in ROOT.rglob('*.md'):
        if any(x in p.parts for x in ('.git', '.venv', '__pycache__')): continue
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' in target or target.startswith(('#','mailto:')): continue
            local = target.split('#',1)[0]
            if local and not (p.parent / local).exists(): failures.append(f'broken link {p.relative_to(ROOT)}: {target}')
    for p in (SKILL / 'assets').rglob('*.json'):
        try: json.loads(p.read_text())
        except (ValueError, OSError) as e: failures.append(f'invalid JSON {p.name}: {e}')
    for p in (SKILL / 'assets/tool-configs').glob('*.json.example'):
        try: json.loads(p.read_text())
        except ValueError as e: failures.append(f'invalid JSON template {p.name}: {e}')
    manifest = ROOT / 'CONTENT_MANIFEST.sha256'
    if manifest.exists():
        for line in manifest.read_text().splitlines():
            digest, rel = line.split('  ', 1)
            p = ROOT / rel
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != digest:
                failures.append(f'manifest mismatch {rel}')
    print(json.dumps({'repository_validation_pass': not failures, 'errors': failures,
                      'artistic_quality': 'not_assessed', 'live_provider_support': 'not_assessed'}, ensure_ascii=False, indent=2))
    return 1 if failures else 0

if __name__ == '__main__':
    sys.exit(validate())
