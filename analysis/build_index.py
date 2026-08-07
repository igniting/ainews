#!/usr/bin/env python3
"""Parse the AI News issues in articles/ into a single index.json.

Each issue carries YAML front matter listing the companies, models, topics and
people that issue covered. Flattening that into one file makes the whole archive
queryable without re-reading 125MB of markdown.
"""

from __future__ import annotations

import datetime as dt
import json
import pathlib
import re
import sys

import yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
ARTICLES = REPO / "articles"
OUT = REPO / "analysis" / "index.json"

FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.DOTALL)
TAG_FIELDS = ("companies", "models", "topics", "people")


def as_list(value: object) -> list[str]:
    """Front matter tags are usually lists but occasionally a bare string."""
    if value is None:
        return []
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return []


def parse_date(meta: dict, path: pathlib.Path) -> str:
    """Prefer the front matter timestamp, fall back to the YY-MM-DD filename."""
    raw = meta.get("date")
    if isinstance(raw, (dt.datetime, dt.date)):
        return raw.date().isoformat() if isinstance(raw, dt.datetime) else raw.isoformat()
    if isinstance(raw, str) and raw.strip():
        try:
            return dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).date().isoformat()
        except ValueError:
            pass
    return f"20{path.name[:8]}".replace("-", "-", 2)


def main() -> int:
    records = []
    skipped = []
    for path in sorted(ARTICLES.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        match = FRONT_MATTER.match(text)
        if not match:
            skipped.append((path.name, "no front matter"))
            continue
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            skipped.append((path.name, f"bad yaml: {exc.__class__.__name__}"))
            continue
        if not isinstance(meta, dict):
            skipped.append((path.name, "front matter is not a mapping"))
            continue

        body = match.group(2)
        record = {
            "file": path.name,
            "date": parse_date(meta, path),
            "title": str(meta.get("title") or "").strip(),
            "slug": str(meta.get("original_slug") or "").strip(),
            "description": str(meta.get("description") or "").strip(),
            "body_chars": len(body),
            "body_words": len(body.split()),
        }
        for field in TAG_FIELDS:
            record[field] = as_list(meta.get(field))
        records.append(record)

    records.sort(key=lambda r: (r["date"], r["file"]))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(records, indent=1) + "\n", encoding="utf-8")

    print(f"indexed {len(records)} issues -> {OUT.relative_to(REPO)}")
    if records:
        print(f"range {records[0]['date']} .. {records[-1]['date']}")
    for name, why in skipped:
        print(f"  skipped {name}: {why}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
