#!/usr/bin/env python3
"""Assemble the standalone 2027 expansion deck.

Inlines the brand font, logo, and the computed dataset into deck.template.html
and writes 2027-expansion-deck.html (fully self-contained, no external hosts).

Rebuild flow:
  1. node scripts/compute.mjs        # sanity-print live Panorama values
  2. node scripts/build_dataset.mjs  # regenerate dataset.json from live data
  3. python3 scripts/build.py        # inline everything -> deck html
"""
import base64, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
tpl  = (ROOT / "deck.template.html").read_text()
font = base64.b64encode((ROOT / "assets/mnkyjane-variable.woff2").read_bytes()).decode()
logo = base64.b64encode((ROOT / "assets/jetson-logo-green.png").read_bytes()).decode()
ds   = (ROOT / "dataset.json").read_text()

out = (tpl.replace("__FONT_B64__", font)
          .replace("__LOGO_B64__", logo)
          .replace("__DATASET__", ds))

for ph in ("__FONT_B64__", "__LOGO_B64__", "__DATASET__"):
    assert ph not in out, f"placeholder {ph} not resolved"

(ROOT / "2027-expansion-deck.html").write_text(out)
print(f"wrote 2027-expansion-deck.html ({round(len(out)/1024)} KB)")
