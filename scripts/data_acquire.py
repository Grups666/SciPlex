"""
SciPlex data acquisition helper.

Downloads publicly reachable data artifacts into the SciPlex object tree and
records provenance, checksum, access metadata, and a data object/state update.
It is generic by design: URLs, filenames, and metadata are inputs. Domain logic
belongs in methods and analysis code, not in this downloader.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from sciplex_runtime import (
    append_event,
    load_state,
    next_object_id,
    save_state,
    sciplex_root,
    write_json,
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_url(url: str, output_path: Path, timeout: int, referer: str | None = None) -> Dict[str, Any]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0 Safari/537.36 SciPlex/0.3"
        ),
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "close",
    }
    if referer:
        headers["Referer"] = referer
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310 - URL is user supplied for data acquisition.
        headers = dict(response.headers.items())
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wb") as fh:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                fh.write(chunk)
    return headers


def load_json_arg(value: str | None) -> Dict[str, Any]:
    if not value:
        return {}
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8-sig"))
    return json.loads(value)


def upsert_data_object(
    root: Path,
    data_id: str | None,
    attrs: Dict[str, Any],
    state_value: str,
    reason: str,
) -> Dict[str, Any]:
    state = load_state(root)
    data_id = data_id or next_object_id(state, "data")
    data_dir = root / "objects" / "data"
    data_path = data_dir / f"{data_id}.json"
    existing = {}
    if data_path.exists():
        existing = json.loads(data_path.read_text(encoding="utf-8-sig"))

    merged_attrs = {}
    merged_attrs.update(existing.get("attributes", {}))
    merged_attrs.update(attrs)
    obj = {
        "id": data_id,
        "type": "data",
        "state": state_value,
        "attributes": merged_attrs,
    }
    write_json(data_path, obj)

    is_new = data_id not in state.get("objects", {})
    state["objects"][data_id] = {"type": "data", "state": state_value, "path": str(data_path.relative_to(root))}
    if is_new:
        state["counts"]["data"] = state["counts"].get("data", 0) + 1
    save_state(root, state)
    append_event(
        root,
        {
            "action": "create" if is_new else "transition",
            "object_id": data_id,
            "object_type": "data",
            "state_after": state_value,
            "reason": reason,
            "details": {"path": str(data_path.relative_to(root))},
        },
    )
    return obj


def record_failed_acquisition(root: Path, data_id: str, url: str, filename: str, error: Exception) -> None:
    state = load_state(root)
    fail_id = next_object_id(state, "failed")
    fail_path = root / "objects" / "failed" / f"{fail_id}.json"
    failure = {
        "id": fail_id,
        "type": "failed",
        "state": "recorded",
        "attributes": {
            "failure_type": "data_acquisition",
            "data_id": data_id,
            "url": url,
            "filename": filename,
            "error": str(error),
            "occurred_at": utc_now(),
            "next_fallbacks": [
                "retry with referer/source landing page",
                "check provider landing page for alternate files or APIs",
                "record documented-statistics synthesis if raw files remain inaccessible",
            ],
        },
    }
    write_json(fail_path, failure)
    state["objects"][fail_id] = {"type": "failed", "state": "recorded", "path": str(fail_path.relative_to(root))}
    state["counts"]["failed"] = state["counts"].get("failed", 0) + 1
    save_state(root, state)
    append_event(
        root,
        {
            "action": "create",
            "object_id": fail_id,
            "object_type": "failed",
            "state_after": "recorded",
            "reason": "Public data acquisition failed",
            "details": {"data_id": data_id, "url": url, "error": str(error)},
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Acquire public data artifacts for SciPlex")
    parser.add_argument("--workspace", default=".", help="Workspace root or sciplex/ directory")
    parser.add_argument("--url", required=True, help="Public URL to download")
    parser.add_argument("--data-id", help="Existing or desired data object id, e.g. data_001")
    parser.add_argument("--filename", help="Output filename. Defaults to URL basename")
    parser.add_argument("--name", help="Human-readable dataset name")
    parser.add_argument("--source", help="Dataset source/organization")
    parser.add_argument("--license", dest="license_value", help="License or terms label if known")
    parser.add_argument("--metadata", help="JSON string or path with additional data object attributes")
    parser.add_argument("--referer", help="Optional source page URL to send as an HTTP Referer")
    parser.add_argument("--timeout", type=int, default=90)
    args = parser.parse_args()

    root = sciplex_root(Path(args.workspace))
    filename = args.filename or Path(args.url.split("?", 1)[0]).name
    if not filename:
        raise ValueError("Could not infer filename from URL; pass --filename")

    state = load_state(root)
    data_id = args.data_id or next_object_id(state, "data")
    rel_output = Path("objects") / "data" / data_id / "raw" / filename
    output_path = root / rel_output
    try:
        headers = download_url(args.url, output_path, args.timeout, args.referer)
    except Exception as exc:
        attrs = load_json_arg(args.metadata)
        attrs.update(
            {
                "name": args.name or attrs.get("name") or data_id,
                "source": args.source or attrs.get("source"),
                "source_url": args.url,
                "license": args.license_value or attrs.get("license"),
                "access_status": "blocked",
                "last_acquisition_error": str(exc),
                "last_attempted_at": utc_now(),
            }
        )
        upsert_data_object(root, data_id, attrs, "identified", "Public data acquisition failed")
        record_failed_acquisition(root, data_id, args.url, filename, exc)
        raise
    checksum = sha256_file(output_path)
    content_type = headers.get("Content-Type") or mimetypes.guess_type(filename)[0]

    manifest = {
        "generated_at": utc_now(),
        "data_id": data_id,
        "url": args.url,
        "file_path": str(rel_output).replace("\\", "/"),
        "filename": filename,
        "bytes": output_path.stat().st_size,
        "sha256": checksum,
        "content_type": content_type,
        "headers": {
            key: value
            for key, value in headers.items()
            if key.lower() in {"content-type", "content-length", "last-modified", "etag"}
        },
        "request": {"referer": args.referer} if args.referer else {},
    }
    manifest_path = root / "objects" / "data" / data_id / "manifest.json"
    write_json(manifest_path, manifest)

    attrs = load_json_arg(args.metadata)
    attrs.update(
        {
            "name": args.name or attrs.get("name") or data_id,
            "source": args.source or attrs.get("source"),
            "source_url": args.url,
            "license": args.license_value or attrs.get("license"),
            "access_status": "acquired",
            "file_path": str(rel_output).replace("\\", "/"),
            "manifest_path": str(manifest_path.relative_to(root)).replace("\\", "/"),
            "sha256": checksum,
            "bytes": output_path.stat().st_size,
            "content_type": content_type,
            "acquired_at": manifest["generated_at"],
        }
    )
    obj = upsert_data_object(root, data_id, attrs, "acquired", "Acquired public data artifact")
    print(json.dumps({"status": "ok", "data_id": data_id, "object": obj, "manifest": manifest}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - command-line helper should surface acquisition failures.
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        raise
