"""
SciPlex literature search helper.

This script performs provider-backed literature discovery and writes a compact
candidate pool that agents can inspect before creating literature objects. It is
generic by design: the query, provider, result count, and output path are inputs;
the script does not know any domain-specific bibliography.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from sciplex_runtime import artifact_path, sciplex_root


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def openalex_search(query: str, per_page: int, email: str | None = None) -> List[Dict[str, Any]]:
    params = {
        "search": query,
        "per-page": str(per_page),
        "sort": "cited_by_count:desc",
    }
    if email:
        params["mailto"] = email
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)

    request = urllib.request.Request(url, headers={"User-Agent": "SciPlex literature_search.py"})
    with urllib.request.urlopen(request, timeout=45) as response:  # noqa: S310 - provider URL is fixed.
        payload = json.loads(response.read().decode("utf-8"))

    candidates = []
    for item in payload.get("results", []):
        authors = [
            author.get("author", {}).get("display_name")
            for author in item.get("authorships", [])[:8]
            if author.get("author", {}).get("display_name")
        ]
        primary_location = item.get("primary_location") or {}
        source = primary_location.get("source") or {}
        candidates.append(
            {
                "provider": "openalex",
                "openalex_id": item.get("id"),
                "doi": item.get("doi"),
                "title": item.get("display_name"),
                "year": item.get("publication_year"),
                "authors": authors,
                "venue": source.get("display_name"),
                "type": item.get("type"),
                "cited_by_count": item.get("cited_by_count"),
                "landing_page_url": primary_location.get("landing_page_url"),
                "abstract_inverted_index_present": bool(item.get("abstract_inverted_index")),
                "concepts": [
                    concept.get("display_name")
                    for concept in item.get("concepts", [])[:8]
                    if concept.get("display_name")
                ],
            }
        )
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Search literature providers for SciPlex")
    parser.add_argument("--workspace", default=".", help="Workspace root or sciplex/ directory")
    parser.add_argument("--query", required=True, help="Provider search query")
    parser.add_argument("--provider", default="openalex", choices=["openalex"])
    parser.add_argument("--per-page", type=int, default=25)
    parser.add_argument("--email", help="Contact email for provider etiquette")
    parser.add_argument("--output", default="literature_candidates.json", help="Output filename under objects/literature/")
    args = parser.parse_args()

    root = sciplex_root(Path(args.workspace))
    if args.provider == "openalex":
        candidates = openalex_search(args.query, args.per_page, args.email)
    else:
        raise ValueError(f"Unsupported provider: {args.provider}")

    output_path = artifact_path(root, "literature", args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": utc_now(),
        "provider": args.provider,
        "query": args.query,
        "count": len(candidates),
        "candidates": candidates,
    }
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "path": str(output_path), "count": len(candidates)}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001 - command-line helper should surface provider failures.
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        raise
