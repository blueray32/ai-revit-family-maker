#!/usr/bin/env python3

import argparse, shutil, os
from pathlib import Path

def main():
    p = argparse.ArgumentParser(description="Deploy PRP templates into a target folder.")
    p.add_argument("--template", default="PRPs/templates/prp_pydantic_ai_base.md", help="Template path")
    p.add_argument("--out", default="PRPs/INITIAL.md", help="Output path")
    args = p.parse_args()

    src = Path(args.template)
    dst = Path(args.out)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"Copied {src} -> {dst}")

if __name__ == "__main__":
    main()
