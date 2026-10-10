"""Hash the tracked package, excluding only the manifest itself.

Run before reproduction: generated result files may legitimately change afterward.
Generation uses the Git index: stage new files before --write. Archive checking
without Git verifies listed bytes only; it cannot establish inventory completeness.
"""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess

ROOT=Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked(root):
    result=subprocess.run(["git","ls-files","-z"],cwd=root,capture_output=True,check=True)
    return sorted(p for p in result.stdout.decode().split("\0") if p and p!="SHA256SUMS")


def generate(root,paths):
    text="".join(f"{digest(root/p)}  {p}\n" for p in sorted(paths))
    (root/"SHA256SUMS").write_text(text)


def verify(root,expected=None):
    entries={}
    for line in (root/"SHA256SUMS").read_text().splitlines():
        match=re.fullmatch(r"([0-9a-f]{64})  (.+)",line)
        if not match: raise ValueError("Malformed manifest line")
        h,name=match.groups();p=Path(name)
        if p.is_absolute() or ".." in p.parts or name=="SHA256SUMS" or name in entries:
            raise ValueError("Unsafe or duplicate manifest path: "+name)
        entries[name]=h
    if not entries: raise ValueError("Empty manifest")
    if expected is not None and set(entries)!=set(expected):
        raise ValueError("Manifest inventory differs from tracked package")
    for name,h in entries.items():
        path=root/name
        if not path.is_file() or digest(path)!=h:
            raise ValueError("Missing or changed package file: "+name)
    return len(entries)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--archive",action="store_true",help="verify listed bytes without Git inventory check")
    args=parser.parse_args()
    if args.write and args.archive: parser.error("--write requires Git inventory")
    paths=None if args.archive else tracked(ROOT)
    if args.write: generate(ROOT,paths)
    print(f"PASS: {verify(ROOT,paths)} package files; "+("listed bytes only" if args.archive else "Git inventory and bytes"))
