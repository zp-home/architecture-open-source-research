#!/usr/bin/env python3
"""Emit a read-only, deterministic inventory of a local codebase as JSON."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

IGNORED = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".pytest_cache"}
MANIFESTS = {"package.json", "pyproject.toml", "requirements.txt", "poetry.lock", "pom.xml", "build.gradle", "go.mod", "Cargo.toml", "Dockerfile", "docker-compose.yml", "docker-compose.yaml"}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--max-files", type=int, default=5000)
    args = parser.parse_args()
    root = Path(args.path).resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")
    files = []
    for item in root.rglob("*"):
        if not item.is_file() or any(part in IGNORED for part in item.relative_to(root).parts):
            continue
        files.append(item)
        if len(files) >= args.max_files:
            break
    files.sort(key=lambda p: str(p.relative_to(root)).lower())
    by_ext = {}
    manifests = []
    total_bytes = 0
    for item in files:
        rel = str(item.relative_to(root)).replace("\\", "/")
        size = item.stat().st_size
        total_bytes += size
        ext = item.suffix.lower() or "[no extension]"
        by_ext[ext] = by_ext.get(ext, 0) + 1
        if item.name in MANIFESTS or item.name.lower().startswith("dockerfile"):
            manifests.append(rel)
    print(json.dumps({"root": str(root), "file_count": len(files), "total_bytes": total_bytes,
                      "extensions": dict(sorted(by_ext.items())), "manifests": manifests,
                      "sample_files": [str(p.relative_to(root)).replace("\\", "/") for p in files[:100]],
                      "truncated": len(files) >= args.max_files,
                      "verification_required": ["Read manifests and source before inferring architecture.", "Check tests, CI, deployment, and license files manually."]}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
