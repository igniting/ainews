#!/usr/bin/env python3
"""Download the Latent Space AI News archive as markdown, one file per issue.

The archive page at https://www.latent.space/s/ainews/archive?sort=new is an
infinite-scroll view over Substack's archive API. This script pages through that
API directly instead of driving a browser, then fetches each post's body and
writes it to disk as markdown with YAML front matter.

Typical use:

    python3 scripts/fetch_ainews.py --since 2026-01-27

Re-running is cheap: issues already on disk are skipped unless --force is given,
so an interrupted run can just be restarted.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys
import time
from typing import Any, Iterator

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify

PUBLICATION = "https://www.latent.space"
SECTION_SLUG = "ainews"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
PAGE_SIZE = 50
RETRY_STATUS = {429, 500, 502, 503, 504}


class FetchError(RuntimeError):
    pass


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    return session


def get(session: requests.Session, url: str, *, tries: int = 5, **kwargs: Any) -> requests.Response:
    """GET with exponential backoff on transient failures."""
    delay = 2.0
    last: Exception | None = None
    for attempt in range(1, tries + 1):
        try:
            response = session.get(url, timeout=60, **kwargs)
            if response.status_code in RETRY_STATUS:
                raise FetchError(f"HTTP {response.status_code} from {url}")
            response.raise_for_status()
            return response
        except (requests.RequestException, FetchError) as exc:
            last = exc
            if attempt == tries:
                break
            sys.stderr.write(f"  retry {attempt}/{tries - 1} after {exc}\n")
            time.sleep(delay)
            delay *= 2
    raise FetchError(f"giving up on {url}: {last}")


# --------------------------------------------------------------------------- #
# Archive listing
# --------------------------------------------------------------------------- #


def in_section(post: dict[str, Any]) -> bool:
    """True if a post belongs to the AI News section.

    Substack exposes the section on the post in a few different shapes depending
    on the endpoint, so check all of them before falling back to the title, which
    every AI News issue prefixes with "[AINews]".
    """
    for key in ("section_slug", "sectionSlug"):
        if post.get(key) == SECTION_SLUG:
            return True
    for key in ("section", "postSection"):
        section = post.get(key)
        if isinstance(section, dict) and section.get("slug") == SECTION_SLUG:
            return True
    return str(post.get("title") or "").lstrip().lower().startswith("[ainews]")


def iter_archive(session: requests.Session, sleep: float) -> Iterator[dict[str, Any]]:
    """Yield archive entries newest first, paging until the API runs dry."""
    offset = 0
    while True:
        url = f"{PUBLICATION}/api/v1/archive"
        params = {"sort": "new", "search": "", "offset": offset, "limit": PAGE_SIZE}
        batch = get(session, url, params=params).json()
        if not batch:
            return
        yield from batch
        offset += len(batch)
        if len(batch) < PAGE_SIZE:
            return
        time.sleep(sleep)


def post_date(post: dict[str, Any]) -> dt.date:
    raw = post.get("post_date") or post.get("published_at") or ""
    return dt.datetime.fromisoformat(raw.replace("Z", "+00:00")).date()


# --------------------------------------------------------------------------- #
# Post bodies
# --------------------------------------------------------------------------- #


def fetch_body_html(session: requests.Session, post: dict[str, Any]) -> str:
    """Return the post body as HTML, preferring the API over page scraping."""
    if post.get("body_html"):
        return post["body_html"]

    slug = post["slug"]
    detail = get(session, f"{PUBLICATION}/api/v1/posts/{slug}").json()
    if detail.get("body_html"):
        return detail["body_html"]

    # Paywalled or otherwise trimmed in the API: fall back to the rendered page.
    page = get(session, post.get("canonical_url") or f"{PUBLICATION}/p/{slug}")
    soup = BeautifulSoup(page.text, "html.parser")
    content = soup.select_one("div.available-content") or soup.select_one("div.body")
    if content is None:
        raise FetchError(f"no body found for {slug}")
    return str(content)


def to_markdown(html: str) -> str:
    markdown = markdownify(html, heading_style="ATX", bullets="-", strip=["script", "style"])
    # markdownify leaves long runs of blank lines where Substack nests divs.
    return re.sub(r"\n{3,}", "\n\n", markdown).strip()


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #


def yaml_quote(value: Any) -> str:
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def render(post: dict[str, Any], body: str) -> str:
    front = {
        "title": post.get("title") or "",
        "subtitle": post.get("subtitle") or "",
        "date": post_date(post).isoformat(),
        "slug": post.get("slug") or "",
        "url": post.get("canonical_url") or f"{PUBLICATION}/p/{post.get('slug')}",
        "source": "latent.space/s/ainews",
    }
    lines = ["---"]
    lines += [f"{key}: {yaml_quote(value)}" for key, value in front.items()]
    lines += ["---", "", f"# {front['title']}", ""]
    if front["subtitle"]:
        lines += [f"*{front['subtitle']}*", ""]
    lines += [body, ""]
    return "\n".join(lines)


def filename(post: dict[str, Any]) -> str:
    return f"{post_date(post).isoformat()}-{post['slug']}.md"


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--since",
        type=dt.date.fromisoformat,
        default=dt.date(2026, 1, 27),
        help="oldest issue date to keep, YYYY-MM-DD (default: 2026-01-27)",
    )
    parser.add_argument("--until", type=dt.date.fromisoformat, help="newest issue date to keep, YYYY-MM-DD")
    parser.add_argument(
        "--out",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parent.parent / "articles",
        help="directory to write markdown into (default: <repo>/articles)",
    )
    parser.add_argument("--force", action="store_true", help="re-download issues already on disk")
    parser.add_argument("--sleep", type=float, default=1.0, help="seconds between requests (default: 1.0)")
    parser.add_argument("--max", type=int, help="stop after downloading this many issues")
    parser.add_argument("--dry-run", action="store_true", help="list what would be downloaded, write nothing")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    session = make_session()
    args.out.mkdir(parents=True, exist_ok=True)

    selected: list[dict[str, Any]] = []
    for post in iter_archive(session, args.sleep):
        try:
            date = post_date(post)
        except ValueError:
            sys.stderr.write(f"skipping {post.get('slug')}: unparseable date\n")
            continue
        if date < args.since:
            break  # archive is newest-first, so everything after this is older
        if args.until and date > args.until:
            continue
        if in_section(post):
            selected.append(post)

    print(f"{len(selected)} AI News issues between {args.since} and {args.until or 'now'}")

    written = 0
    for post in selected:
        if args.max is not None and written >= args.max:
            break
        target = args.out / filename(post)
        if target.exists() and not args.force:
            continue
        if args.dry_run:
            print(f"would write {target.name}")
            written += 1
            continue
        try:
            body = fetch_body_html(session, post)
        except FetchError as exc:
            sys.stderr.write(f"FAILED {post.get('slug')}: {exc}\n")
            continue
        target.write_text(render(post, to_markdown(body)), encoding="utf-8")
        written += 1
        print(f"wrote {target.name}")
        time.sleep(args.sleep)

    if not args.dry_run:
        index = [
            {
                "date": post_date(post).isoformat(),
                "title": post.get("title"),
                "slug": post.get("slug"),
                "url": post.get("canonical_url"),
                "file": filename(post),
            }
            for post in selected
        ]
        (args.out / "index.json").write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")

    print(f"done: {written} new file(s) in {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
