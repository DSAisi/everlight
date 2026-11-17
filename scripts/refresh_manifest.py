from pathlib import Path
import hashlib,json,subprocess
p=Path(__file__).resolve().parents[1]
try:
    output=subprocess.check_output(['git','ls-files','-co','--exclude-standard','-z'],cwd=p,stderr=subprocess.DEVNULL)
    paths=[p/name for name in output.decode().split('\0') if name]
except (FileNotFoundError,subprocess.CalledProcessError):
    paths=[f for f in p.rglob('*') if not any(x in {'.git','__pycache__','.venv'} for x in f.relative_to(p).parts)]
sha={}
for f in sorted(set(paths)):
    if f.is_file() and not f.is_symlink() and f!=p/'manifest.json':
        sha[f.relative_to(p).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
(p/'manifest.json').write_text(json.dumps({'version':'Universal repository 1.0','production_approved':False,'sha256':sha},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
