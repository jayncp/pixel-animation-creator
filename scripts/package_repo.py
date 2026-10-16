#!/usr/bin/env python3
"""Package a clean repository with sanitized, real Git history; no network."""
import argparse, hashlib, os, pathlib, subprocess, sys, tempfile, zipfile
ROOT = pathlib.Path(__file__).resolve().parents[1]

def run(*args, cwd=ROOT):
    return subprocess.check_output(args, cwd=cwd, text=True, stderr=subprocess.STDOUT).strip()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('output'); a = ap.parse_args()
    out = pathlib.Path(a.output).expanduser().resolve()
    if out.exists(): raise SystemExit('Refusing existing output; choose a new release path.')
    if out == ROOT or ROOT in out.parents: raise SystemExit('Choose an output outside the source repository.')
    if run('git', 'status', '--porcelain'): raise SystemExit('Commit all intended changes; source tree must be clean.')
    subprocess.run([sys.executable, str(ROOT/'scripts/validate_repo.py')], check=True)
    with tempfile.TemporaryDirectory(prefix='pixel-skill-release-') as tmp:
        copy = pathlib.Path(tmp) / 'pixel-character-animation-repo'
        # clone locally without reusing hardlinks; it carries history without source config/hooks.
        run('git', '-c', 'protocol.file.allow=always', 'clone', '--no-local', '--no-hardlinks', str(ROOT), str(copy))
        run('git', 'remote', 'remove', 'origin', cwd=copy)
        for p in (copy/'.git/hooks').glob('*'):
            if p.is_file(): p.unlink()  # only generated clone sample hooks, never source files
        # Generated reflogs expose local machine paths and are unnecessary for reachable history.
        import shutil
        shutil.rmtree(copy/'.git/logs', ignore_errors=True)
        run('git', 'fsck', '--full', cwd=copy)
        if run('git', 'status', '--porcelain', cwd=copy): raise SystemExit('Release clone unexpectedly dirty.')
        out.parent.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(out, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for p in sorted(copy.rglob('*')):
                if p.is_symlink(): raise SystemExit(f'Release symlink unsupported: {p.relative_to(copy)}')
                if p.is_file(): z.write(p, (pathlib.Path(copy.name)/p.relative_to(copy)).as_posix())
    print(f'{hashlib.sha256(out.read_bytes()).hexdigest()}  {out.name}')
    print(f'bytes={out.stat().st_size}')

if __name__ == '__main__': main()
