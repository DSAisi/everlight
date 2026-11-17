"""Run repository checks without editing the tracked release snapshots."""
from pathlib import Path
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
for command in (
    ['verify_universal.py'],
    ['-m','unittest','discover','-s','reference','-v'],
    ['-m','unittest','discover','-s','examples','-v'],
):
    subprocess.run([sys.executable,*command],cwd=ROOT,env=env,check=True)
