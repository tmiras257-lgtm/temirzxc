#!/usr/bin/env python3
"""Build the Claude-artifact version of bulking from index.html.

The artifact publisher wraps the page in its own <!doctype>/<html>/<head>/<body>
skeleton and pads :root by the safe-area insets, so this strips the document
wrapper, the PWA links and the duplicate top inset.

Usage: python3 build-claude.py OUTPUT.html
"""
import re
import sys
from pathlib import Path

src = (Path(__file__).parent / "index.html").read_text(encoding="utf-8")

head = re.search(r"<head>(.*?)</head>", src, re.S).group(1)
body = re.search(r"<body>(.*?)</body>", src, re.S).group(1)

keep = []
for line in head.strip().splitlines():
    l = line.strip()
    if l.startswith(("<meta charset", '<meta name="viewport"', "<meta name=\"apple", "<meta name=\"mobile",
                     '<link rel="manifest"', '<link rel="icon"', '<link rel="apple-touch-icon"', '<meta name="theme-color"')):
        continue
    keep.append(line)

out = "\n".join(keep)
out = out.replace("<title>bulking</title>",
                  '<title>bulking</title>\n<meta name="claude:viewport-fit-sides" content="cover">', 1)
out = out.replace("padding-top:calc(env(safe-area-inset-top) + 12px)", "padding-top:12px", 1)
out += "\n" + body.strip() + "\n"

for bad in ("<!doctype", "<html", "<head>", "<body>"):
    assert bad not in out.lower(), bad
Path(sys.argv[1]).write_text(out, encoding="utf-8")
print("wrote", sys.argv[1], len(out), "bytes")
