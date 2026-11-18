#!/usr/bin/env python3
"""Generate smaller WebP display copies; never modify source photographs."""
from pathlib import Path
from PIL import Image, ImageOps
ROOT = Path(__file__).resolve().parents[1]
sources = sorted((ROOT / "media").rglob("*"))
count = 0
for src in sources:
    if src.suffix.lower() not in (".jpg", ".jpeg", ".png") or src.name.startswith("map-marker"):
        continue
    if "optimized" in src.parts:
        continue
    rel = src.relative_to(ROOT / "media")
    for category, max_width, quality in (("thumb", 900, 78), ("background", 1800, 82)):
        dst = ROOT / "media" / "optimized" / category / rel.with_suffix(".webp")
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as original:
            im = ImageOps.exif_transpose(original).convert("RGB")
            im.thumbnail((max_width, max_width * 3), Image.Resampling.LANCZOS)
            im.save(dst, "WEBP", quality=quality, method=6)
        count += 1
print(f"Generated {count} WebP display images; originals unchanged.")
