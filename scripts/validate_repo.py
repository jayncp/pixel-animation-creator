#!/usr/bin/env python3
"""Check the skill frontmatter against the Agent Skills spec, local Markdown links and JSON files. Does not certify artwork."""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/pixel-character-animation'
FIELDS = {'name', 'description', 'license', 'compatibility', 'metadata', 'allowed-tools'}

def frontmatter_errors():
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    if not text.startswith('---\n') or '\n---\n' not in text[4:]:
        return ['SKILL.md must start with a --- frontmatter block']
    block = text[4:text.index('\n---\n', 4)]
    fields = dict(re.findall(r'^([A-Za-z-]+):[ \t]*(.*)$', block, re.M))
    errors = [f'unknown frontmatter field {k}' for k in fields if k not in FIELDS]
    name, description = fields.get('name', ''), fields.get('description', '')
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', name) or len(name) > 64 or name != SKILL.name:
        errors.append(f'name must be lowercase-hyphenated, at most 64 characters and match the directory: {name!r}')
    if not 1 <= len(description) <= 1024:
        errors.append('description must be 1-1024 characters')
    if len(fields.get('compatibility', '')) > 500:
        errors.append('compatibility must be at most 500 characters')
    return errors

def validate():
    failures = frontmatter_errors()
    for p in ROOT.rglob('*.md'):
        if any(x in p.parts for x in ('.git', '.venv', '__pycache__')): continue
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
            local = target.split('#', 1)[0]
            if '://' in target or target.startswith(('#', 'mailto:')) or not local: continue
            if not (p.parent / local).exists(): failures.append(f'broken link {p.relative_to(ROOT)}: {target}')
    for p in [*ROOT.rglob('*.json'), *ROOT.rglob('*.json.example')]:
        if '.git' in p.parts or '.venv' in p.parts: continue
        try: json.loads(p.read_text(encoding='utf-8'))
        except ValueError as e: failures.append(f'invalid JSON {p.relative_to(ROOT)}: {e}')
    print(json.dumps({'repository_validation_pass': not failures, 'errors': failures, 'artistic_quality': 'not_assessed'}, indent=2))
    return 1 if failures else 0

if __name__ == '__main__':
    sys.exit(validate())
