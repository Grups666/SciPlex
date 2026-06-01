"""
SciPlex literature metadata audit helper.

The helper verifies cited literature object metadata against provider records
when stable provider IDs are available. It is intentionally domain-neutral:
it compares object metadata to provider metadata and reports discrepancies.
It does not decide which sources are scientifically important.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from sciplex_runtime import load_state, sciplex_root


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_words(value: str) -> List[str]:
    return [word for word in re.findall(r"[a-z0-9]+", value.lower()) if word not in STOPWORDS]


def title_similarity(left: str, right: str) -> float:
    left_words = set(normalize_words(left))
    right_words = set(normalize_words(right))
    if not left_words or not right_words:
        return 0.0
    return len(left_words & right_words) / len(left_words | right_words)


def fetch_openalex(openalex_id: str) -> Dict[str, Any]:
    work_id = openalex_id.rstrip("/").rsplit("/", 1)[-1]
    url = f"https://api.openalex.org/works/{work_id}"
    request = urllib.request.Request(url, headers={"User-Agent": "SciPlex audit_literature.py"})
    with urllib.request.urlopen(request, timeout=45) as response:  # noqa: S310 - provider URL is fixed.
        return json.loads(response.read().decode("utf-8"))


def fetch_openalex_url(url: str) -> Dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "SciPlex audit_literature.py"})
    with urllib.request.urlopen(request, timeout=45) as response:  # noqa: S310 - provider URL is fixed.
        return json.loads(response.read().decode("utf-8"))


def fetch_openalex_by_doi(doi: str) -> Dict[str, Any] | None:
    clean_doi = doi.lower().replace("https://doi.org/", "").replace("http://doi.org/", "").strip()
    if not clean_doi:
        return None
    url = "https://api.openalex.org/works?filter=doi:" + urllib.parse.quote(clean_doi, safe="/:")
    payload = fetch_openalex_url(url)
    results = payload.get("results") or []
    return results[0] if results else None


def fetch_openalex_by_title(title: str) -> Dict[str, Any] | None:
    if not title:
        return None
    url = "https://api.openalex.org/works?search.title=" + urllib.parse.quote(title) + "&per-page=5"
    payload = fetch_openalex_url(url)
    candidates = payload.get("results") or []
    if not candidates:
        return None
    ranked = sorted(candidates, key=lambda item: title_similarity(title, str(item.get("display_name") or "")), reverse=True)
    best = ranked[0]
    if title_similarity(title, str(best.get("display_name") or "")) < 0.55:
        return None
    return best


def audit_literature_object(root: Path, object_id: str, object_path: Path) -> Dict[str, Any]:
    obj = read_json(object_path)
    attrs = obj.get("attributes", {})
    audit: Dict[str, Any] = {
        "id": object_id,
        "status": "unchecked",
        "issues": [],
        "object_metadata": {
            "title": attrs.get("title"),
            "year": attrs.get("year"),
            "doi": attrs.get("doi"),
            "venue": attrs.get("venue"),
            "openalex_id": attrs.get("openalex_id"),
        },
    }
    openalex_id = attrs.get("openalex_id")
    object_title = str(attrs.get("title") or "")
    object_doi = str(attrs.get("doi") or "")
    provider = None
    retrieval_method = None
    fetch_errors = []

    if openalex_id:
        try:
            provider = fetch_openalex(str(openalex_id))
            retrieval_method = "openalex_id"
        except Exception as exc:  # noqa: BLE001 - fall through to DOI/title repair attempts.
            fetch_errors.append({"method": "openalex_id", "error": str(exc)})

    if provider is None and object_doi:
        try:
            provider = fetch_openalex_by_doi(object_doi)
            retrieval_method = "doi" if provider else None
            if provider and object_title and title_similarity(object_title, str(provider.get("display_name") or "")) < 0.55:
                fetch_errors.append(
                    {
                        "method": "doi",
                        "error": "provider record title did not match object title",
                        "provider_title": provider.get("display_name"),
                    }
                )
                provider = None
                retrieval_method = None
        except Exception as exc:  # noqa: BLE001 - fall through to title search.
            fetch_errors.append({"method": "doi", "error": str(exc)})

    if provider is None and object_title:
        try:
            provider = fetch_openalex_by_title(object_title)
            retrieval_method = "title"
        except Exception as exc:  # noqa: BLE001 - report after all fallbacks fail.
            fetch_errors.append({"method": "title", "error": str(exc)})

    if provider is None:
        audit["status"] = "error"
        audit["issues"].append({"severity": "major", "issue": "provider fetch failed", "errors": fetch_errors})
        return audit

    provider_source = ((provider.get("primary_location") or {}).get("source") or {}).get("display_name")
    provider_metadata = {
        "title": provider.get("display_name"),
        "year": provider.get("publication_year"),
        "doi": provider.get("doi"),
        "venue": provider_source,
        "openalex_id": provider.get("id"),
    }
    audit["provider_metadata"] = provider_metadata
    audit["retrieval_method"] = retrieval_method
    if fetch_errors:
        audit["fetch_errors"] = fetch_errors

    provider_title = str(provider_metadata.get("title") or "")
    if title_similarity(object_title, provider_title) < 0.55:
        audit["issues"].append(
            {
                "severity": "major",
                "issue": "title mismatch",
                "object_title": object_title,
                "provider_title": provider_title,
                "similarity": round(title_similarity(object_title, provider_title), 3),
            }
        )

    object_year = attrs.get("year")
    provider_year = provider_metadata.get("year")
    if object_year and provider_year and int(object_year) != int(provider_year):
        year_delta = abs(int(object_year) - int(provider_year))
        audit["issues"].append(
            {
                "severity": "minor" if year_delta == 1 else "major",
                "issue": "year mismatch",
                "object_year": object_year,
                "provider_year": provider_year,
                "note": "A one-year difference can reflect online-first versus issue publication year."
                if year_delta == 1
                else "Larger year differences require citation metadata repair.",
            }
        )

    object_doi = str(attrs.get("doi") or "").lower().replace("https://doi.org/", "")
    provider_doi = str(provider_metadata.get("doi") or "").lower().replace("https://doi.org/", "")
    if object_doi and provider_doi and object_doi != provider_doi:
        audit["issues"].append(
            {
                "severity": "major",
                "issue": "doi mismatch",
                "object_doi": attrs.get("doi"),
                "provider_doi": provider_metadata.get("doi"),
            }
        )

    audit["status"] = "fail" if any(issue["severity"] == "major" for issue in audit["issues"]) else "pass"
    return audit


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit SciPlex literature objects against provider metadata")
    parser.add_argument("--workspace", default=".", help="Workspace root or sciplex/ directory")
    parser.add_argument("--output", default="objects/literature/literature_audit_openalex.json")
    args = parser.parse_args()

    root = sciplex_root(Path(args.workspace))
    state = load_state(root)
    audits = []
    for object_id, meta in sorted(state.get("objects", {}).items()):
        if meta.get("type") != "literature":
            continue
        object_path = root / meta.get("path", f"objects/literature/{object_id}.json")
        audits.append(audit_literature_object(root, object_id, object_path))

    status = "pass" if not any(
        any(issue.get("severity") == "major" for issue in audit.get("issues", [])) for audit in audits
    ) else "fail"
    payload = {
        "generated_at": utc_now(),
        "provider": "openalex",
        "status": status,
        "count": len(audits),
        "audits": audits,
    }
    output_path = root / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": status, "path": str(output_path), "count": len(audits)}, indent=2))
    if status != "pass":
        sys.exit(1)


if __name__ == "__main__":
    main()
