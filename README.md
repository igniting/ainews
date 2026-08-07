# ainews

Tooling to mirror the [Latent Space AI News](https://www.latent.space/s/ainews/archive?sort=new)
daily archive as markdown, one file per issue, so the issues can be analyzed offline.

## Fetching

```bash
pip install -r requirements.txt
python3 scripts/fetch_ainews.py --since 2026-01-27
```

Issues land in `articles/` as `YYYY-MM-DD-<slug>.md` with YAML front matter
(`title`, `subtitle`, `date`, `slug`, `url`, `source`), alongside an
`articles/index.json` manifest of everything the run matched.

The archive page is infinite-scroll, but it is backed by Substack's archive API,
so the script pages through `/api/v1/archive` rather than driving a browser. It
keeps posts in the `ainews` section (falling back to the `[AINews]` title prefix
that every issue uses) and stops as soon as it walks past `--since`, since the
API returns newest-first.

Useful flags:

| flag | effect |
| --- | --- |
| `--since` / `--until` | date window, `YYYY-MM-DD` (default since 2026-01-27) |
| `--dry-run` | list what would be downloaded, write nothing |
| `--max N` | stop after N issues |
| `--force` | re-download issues already on disk |
| `--sleep` | seconds between requests (default 1.0) |

Re-running skips issues already present, so an interrupted run can just be
restarted.

## Network access

`www.latent.space` must be reachable from wherever the script runs. Some sandboxed
environments allow egress only to an allowlist of hosts; there the run fails with
`Tunnel connection failed: 403 Forbidden` and the fetch has to happen somewhere
with open egress.
