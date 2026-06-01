"""
SciPlex runtime helper.

This module handles research bookkeeping that should be deterministic:
workspace initialization, layered config snapshots, object creation, event
logging, and state index updates. It deliberately avoids scientific judgment.
Agents decide what to study, what an object means, and when a transition is
scientifically justified.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


OBJECT_TYPES = {
    "orchestrator": "orch",
    "hypothesis": "hyp",
    "problem": "prob",
    "literature": "lit",
    "data": "data",
    "method": "meth",
    "strategy": "strat",
    "experiment": "exp",
    "figure": "fig",
    "finding": "find",
    "failed": "fail",
    "paper": "paper",
    "console": "console",
    "review": "rev",
}

OBJECT_DIRS = list(OBJECT_TYPES)

ALLOWED_STATES = {
    "orchestrator": {"formulating", "designing", "executing", "synthesizing", "writing", "complete"},
    "hypothesis": {"formulated", "tested", "supported", "refuted", "inconclusive"},
    "problem": {"identified", "resolved"},
    "literature": {"identified", "read", "cited", "validated"},
    "data": {"identified", "acquired", "validated", "processed"},
    "method": {"designed", "implemented", "validated"},
    "strategy": {"evaluated", "active"},
    "experiment": {"running", "designed", "completed", "failed"},
    "figure": {"draft", "finalized"},
    "finding": {"draft", "validated"},
    "failed": {"recorded"},
    "paper": {"draft", "reviewed", "final"},
    "console": {"active"},
    "review": {"completed"},
}

ROOT_ALLOWED_ENTRIES = {
    ".sciplex",
    "context.md",
    "config",
    "state.json",
    "events.json",
    "objects",
}

WORKSPACE_CONTRACT_VERSION = "0.3"

OUTPUT_STANDARDS = {
    "brief": {"min_words": 800, "max_words": 1500, "min_references": 5, "min_figures": 0, "min_source_roles": 2},
    "report": {"min_words": 3000, "max_words": 6000, "min_references": 15, "min_figures": 3, "min_source_roles": 4},
    "paper": {"min_words": 7000, "max_words": 10000, "min_references": 25, "min_figures": 4, "min_source_roles": 5, "count_basis": "main_text"},
    "protocol": {"min_words": 1500, "max_words": 5000, "min_references": 8, "min_figures": 0, "min_source_roles": 3},
    "registered_report": {"min_words": 3000, "max_words": 7000, "min_references": 15, "min_figures": 0, "min_source_roles": 4},
    "console_audit": {"min_words": 0, "max_words": 0, "min_references": 0, "min_figures": 0, "min_source_roles": 0},
}

PAPER_SECTION_MIN_WORDS = {
    "introduction": 900,
    "literature_background": 900,
    "methods_data": 800,
    "results": 900,
    "discussion": 800,
    "conclusion": 250,
}

REVIEW_DIMENSIONS = {
    "method_fidelity",
    "evidence_chain",
    "claim_validity",
    "source_coverage",
    "result_consistency",
    "output_standards",
    "limitations",
    "overclaim",
}

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
    "into",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "under",
    "with",
}

CONFIG_KEYS = [
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "SCIPLEX_LLM_DEFAULT",
    "SCIPLEX_LLM_LITERATURE",
    "SCIPLEX_LLM_METHOD",
    "SCIPLEX_LLM_REVIEW",
    "SCIPLEX_LLM_WRITING",
    "SCIPLEX_OUTPUT_TARGET",
    "SCIPLEX_REPORT_WORDS",
    "SCIPLEX_PAPER_WORDS",
    "SCIPLEX_PAPER_MAIN_FIGURES",
    "SCIPLEX_PAPER_REFERENCES",
    "SCIPLEX_DEFAULT_EVIDENCE_MODE",
    "RESEARCH_CONTACT_EMAIL",
    "ENABLE_OPENALEX",
    "ENABLE_ARXIV",
    "ENABLE_ZOTERO",
    "OPENALEX_BASE_URL",
    "OPENALEX_EMAIL",
    "SEMANTIC_SCHOLAR_API_KEY",
    "ZOTERO_USER_ID",
    "ZOTERO_API_KEY",
    "NCBI_API_KEY",
    "PROVIDER_TIMEOUT_SECONDS",
]

SECRET_HINTS = ("KEY", "TOKEN", "SECRET", "PASSWORD")

FORWARD_PHASES = [
    "IDLE",
    "FORMULATING",
    "REVIEWING_LITERATURE",
    "DESIGNING_METHODS",
    "PREPARING_DATA",
    "RUNNING_EXPERIMENTS",
    "VALIDATING_RESULTS",
    "SYNTHESIZING",
    "WRITING",
    "REVIEWING",
    "COMPLETE",
]

SPECIAL_PHASES = {"ITERATING", "REFRAMING"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_words(value: str) -> List[str]:
    return [word for word in re.findall(r"[a-z0-9]+", value.lower()) if word not in STOPWORDS]


def title_signature(title: str, limit: int = 5) -> List[str]:
    return normalize_words(title)[:limit]


def has_title_signature(text: str, title: str) -> bool:
    signature = title_signature(title)
    if len(signature) < 2:
        return True
    text_words = set(normalize_words(text))
    matched = sum(1 for word in signature if word in text_words)
    return matched >= min(3, len(signature))


def author_year_mentioned(text: str, attrs: Dict[str, Any]) -> bool:
    year = str(attrs.get("year") or "")
    authors = attrs.get("authors") or []
    first_author = ""
    if authors:
        first_author = str(authors[0]).split(",")[0].split()[-1]
    if first_author and year:
        author_pattern = re.escape(first_author)
        year_pattern = re.escape(year)
        if re.search(author_pattern + r".{0,60}" + year_pattern, text, re.IGNORECASE | re.DOTALL):
            return True
        if re.search(author_pattern, text, re.IGNORECASE) and year in text:
            return True
    title = str(attrs.get("title") or "")
    title_terms = [word for word in normalize_words(title) if len(word) > 4][:4]
    if title_terms and sum(1 for word in title_terms if re.search(re.escape(word), text, re.IGNORECASE)) >= min(2, len(title_terms)):
        return True
    return False


def stable_link_tokens(attrs: Dict[str, Any]) -> List[str]:
    tokens: List[str] = []
    for key in ["doi", "url", "source_url", "openalex_id", "arxiv_id", "pmid", "nber_id"]:
        value = str(attrs.get(key) or "").strip()
        if not value:
            continue
        lower_value = value.lower()
        tokens.append(lower_value)
        if lower_value.startswith("https://doi.org/"):
            tokens.append(lower_value.replace("https://doi.org/", ""))
        elif lower_value.startswith("http://doi.org/"):
            tokens.append(lower_value.replace("http://doi.org/", ""))
        elif "/" not in lower_value and lower_value.startswith("10."):
            tokens.append("https://doi.org/" + lower_value)
    return [token for token in tokens if token]


def has_stable_link(text: str, attrs: Dict[str, Any]) -> bool:
    lower_text = text.lower()
    return any(token in lower_text for token in stable_link_tokens(attrs))


def markdown_linked_author_year(text: str, attrs: Dict[str, Any]) -> bool:
    year = str(attrs.get("year") or "")
    authors = attrs.get("authors") or []
    if not year or not authors:
        return has_stable_link(text, attrs)
    first_author = str(authors[0]).split(",")[0].split()[-1]
    if not first_author:
        return has_stable_link(text, attrs)
    # Markdown link text containing author and year with a nearby href matching
    # a stable identifier. The nearby-window check handles DOI URLs that contain
    # parentheses, which simple Markdown regexes often truncate.
    for match in re.finditer(r"\[([^\]]+)\]\(", text, re.IGNORECASE | re.DOTALL):
        label = match.group(1)
        if re.search(re.escape(first_author), label, re.IGNORECASE) and year in label:
            nearby = text[match.start() : match.start() + 500].lower()
            if any(token in nearby for token in stable_link_tokens(attrs)):
                return True
    return False


def count_words(value: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", value))


def manuscript_regions(text: str) -> Dict[str, Any]:
    heading_matches = list(re.finditer(r"(?m)^##\s+(.+?)\s*$", text))
    references_match = re.search(r"(?im)^##\s+references\s*$", text)
    appendix_match = re.search(r"(?im)^##\s+append(?:ix|ices)?\b", text)
    main_end_candidates = [
        match.start()
        for match in [references_match, appendix_match]
        if match is not None
    ]
    main_end = min(main_end_candidates) if main_end_candidates else len(text)
    intro_match = re.search(r"(?im)^##\s+(?:\d+\.?\s*)?introduction\b", text)
    main_start = intro_match.start() if intro_match else 0
    main_text = text[main_start:main_end]
    references_end = appendix_match.start() if references_match and appendix_match and appendix_match.start() > references_match.start() else len(text)
    reference_text = text[references_match.end():references_end] if references_match else ""
    appendix_text = text[appendix_match.start():] if appendix_match else ""
    sections: List[Dict[str, Any]] = []
    for idx, match in enumerate(heading_matches):
        start = match.end()
        end = heading_matches[idx + 1].start() if idx + 1 < len(heading_matches) else len(text)
        sections.append({"heading": match.group(1).strip(), "text": text[start:end], "start": match.start()})
    return {
        "main_text": main_text,
        "reference_text": reference_text,
        "appendix_text": appendix_text,
        "sections": sections,
        "main_word_count": count_words(main_text),
        "reference_word_count": count_words(reference_text),
        "appendix_word_count": count_words(appendix_text),
    }


def paper_section_word_counts(sections: List[Dict[str, Any]]) -> Dict[str, int]:
    counts = {
        "introduction": 0,
        "literature_background": 0,
        "methods_data": 0,
        "results": 0,
        "discussion": 0,
        "conclusion": 0,
    }
    for section in sections:
        heading = str(section.get("heading") or "").lower()
        count = count_words(str(section.get("text") or ""))
        if "reference" in heading or "appendix" in heading:
            continue
        if "introduction" in heading:
            counts["introduction"] += count
        elif any(token in heading for token in ["literature", "background", "evidence frame", "related work", "evidence review"]):
            counts["literature_background"] += count
        elif any(token in heading for token in ["method", "data", "material", "empirical strategy"]):
            counts["methods_data"] += count
        elif any(token in heading for token in ["result", "finding", "analysis"]):
            counts["results"] += count
        elif any(token in heading for token in ["discussion", "limitation", "interpretation", "robustness"]):
            counts["discussion"] += count
        elif "conclusion" in heading:
            counts["conclusion"] += count
    return counts


def numbered_section_order_problem(sections: List[Dict[str, Any]]) -> List[int]:
    numbers = []
    for section in sections:
        match = re.match(r"\s*(\d+)\.", str(section.get("heading") or ""))
        if match:
            numbers.append(int(match.group(1)))
    if numbers and numbers != sorted(numbers):
        return numbers
    return []


def write_json(path: Path, value: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def parse_env_file(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip().lstrip("\ufeff")] = value.strip().strip('"').strip("'")
    return values


def parse_simple_yaml(path: Path) -> Dict[str, str]:
    values: Dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line or line.startswith("-"):
            continue
        key, value = line.split(":", 1)
        key = key.strip().lstrip("\ufeff")
        value = value.strip().strip('"').strip("'")
        if key and value:
            values[key] = value
    return values


def merge_layers(layers: Iterable[Tuple[str, Dict[str, str]]]) -> Dict[str, Dict[str, str]]:
    resolved: Dict[str, Dict[str, str]] = {}
    for source, values in reversed(list(layers)):
        for key, value in values.items():
            if key in CONFIG_KEYS and value != "":
                resolved[key] = {"source": source, "value": value}
    return resolved


def redact(key: str, value: str) -> str:
    if any(hint in key.upper() for hint in SECRET_HINTS):
        return "<redacted>"
    return "<set>" if value else "<unset>"


def is_enabled(value: str) -> bool:
    return value.lower() not in {"false", "0", "no", "off", "disabled"}


def provider_status(resolved: Dict[str, Dict[str, str]]) -> Dict[str, str]:
    def value(key: str) -> str:
        return resolved.get(key, {}).get("value", "")

    return {
        "openalex": "enabled" if is_enabled(value("ENABLE_OPENALEX")) else "disabled",
        "arxiv": "enabled" if is_enabled(value("ENABLE_ARXIV")) else "disabled",
        "zotero": "enabled"
        if is_enabled(value("ENABLE_ZOTERO")) and value("ZOTERO_USER_ID") and value("ZOTERO_API_KEY")
        else "disabled",
        "semantic_scholar": "enabled" if value("SEMANTIC_SCHOLAR_API_KEY") else "degraded",
        "ncbi": "enabled" if value("NCBI_API_KEY") else "degraded",
    }


def sciplex_root(workspace: Path) -> Path:
    root = workspace.resolve()
    return root if root.name == "sciplex" else root / "sciplex"


def state_path(root: Path) -> Path:
    return root / "state.json"


def events_path(root: Path) -> Path:
    return root / "events.json"


def contract_path(root: Path) -> Path:
    return root / ".sciplex"


def context_path(root: Path) -> Path:
    return root / "context.md"


def default_state() -> Dict[str, Any]:
    return {
        "objects": {},
        "counts": {name: 0 for name in OBJECT_DIRS},
        "current_phase": "IDLE",
        "last_updated": utc_now(),
    }


def load_state(root: Path) -> Dict[str, Any]:
    state = read_json(state_path(root), default_state())
    state.setdefault("objects", {})
    state.setdefault("counts", {})
    state.setdefault("current_phase", "IDLE")
    for object_type in OBJECT_DIRS:
        state["counts"].setdefault(object_type, 0)
    return state


def save_state(root: Path, state: Dict[str, Any]) -> None:
    state["last_updated"] = utc_now()
    write_json(state_path(root), state)


def append_event(root: Path, event: Dict[str, Any]) -> Dict[str, Any]:
    event = {"timestamp": utc_now(), **event}
    log = read_json(events_path(root), {"events": []})
    log.setdefault("events", []).append(event)
    write_json(events_path(root), log)
    return event


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def workspace_contract() -> Dict[str, Any]:
    return {
        "schema": "sciplex-workspace",
        "version": WORKSPACE_CONTRACT_VERSION,
        "artifact_root": "objects",
        "config_root": "config",
        "rules": [
            "All research artifacts must be written under objects/<object_type>/.",
            "Only config, state.json, events.json, .sciplex, context.md, and objects belong at the sciplex root.",
            "Create or update objects through sciplex_runtime.py when possible so state.json and events.json stay synchronized.",
            "If raw data is not acquired and processed, label the study as evidence synthesis or scoping analysis, not completed empirical analysis.",
            "Final outputs must document source coverage, evidence chains, limitations, and output-target standards.",
            "Before writing files, load this contract and context.md to recover workspace paths, output target, and evidence requirements.",
        ],
        "object_types": sorted(OBJECT_TYPES),
    }


def default_context() -> str:
    return """# SciPlex Workspace Context

Load this file before creating, reading, or updating research artifacts.

## Path Rules

- Workspace root: this `sciplex/` directory.
- Research artifacts: `objects/<object_type>/`.
- Project configuration: `config/`.
- Do not create research artifact folders directly under `sciplex/`.

## Evidence Rules

- Distinguish raw-data analysis from literature/documented-statistics synthesis.
- Claims must state their evidence mode and limitations.
- A major unresolved data-access gap blocks claims of completed empirical analysis.
- Final outputs should include source coverage, counterevidence, and evidence chains.

## Output Target

Set the intended output target in a strategy, orchestrator, or paper/report
object before writing. Examples: report, paper, brief, protocol, console.
"""


def resolve_config(root: Path, skill_root: Path) -> Dict[str, Any]:
    config_dir = root / "config"
    layers = [
        ("project_env", parse_env_file(config_dir / ".env.local")),
        ("project_config_yaml", parse_simple_yaml(config_dir / "config.yaml")),
        ("skill_env", parse_env_file(skill_root / "config" / ".env.local")),
        ("skill_config_yaml", parse_simple_yaml(skill_root / "config" / "config.yaml")),
        ("driver_env", {key: os.environ.get(key, "") for key in CONFIG_KEYS}),
    ]
    resolved = merge_layers(layers)
    return {
        "generated_at": utc_now(),
        "precedence": [
            "project_env",
            "project_config_yaml",
            "skill_env",
            "skill_config_yaml",
            "driver_env",
            "built_in_defaults",
        ],
        "values": {
            key: {"source": item["source"], "value": redact(key, item["value"])}
            for key, item in sorted(resolved.items())
        },
        "providers": provider_status(resolved),
        "notes": [
            "config.yaml layers use a conservative flat key: value parser.",
            "Secrets are redacted and must not be copied into research objects.",
        ],
    }


def initialize_workspace(workspace: Path, skill_root: Path) -> Path:
    root = sciplex_root(workspace)
    (root / "config").mkdir(parents=True, exist_ok=True)
    (root / "objects").mkdir(parents=True, exist_ok=True)
    for object_type in OBJECT_DIRS:
        (root / "objects" / object_type).mkdir(parents=True, exist_ok=True)

    write_if_missing(contract_path(root), json.dumps(workspace_contract(), indent=2) + "\n")
    write_if_missing(context_path(root), default_context())
    write_if_missing(root / "config" / ".env.local", "# Project-level private SciPlex overrides. Do not commit secrets.\n")
    write_if_missing(root / "config" / "config.yaml", "# Project-level non-secret SciPlex settings.\n")
    write_if_missing(state_path(root), json.dumps(default_state(), indent=2) + "\n")
    write_if_missing(events_path(root), json.dumps({"events": []}, indent=2) + "\n")

    write_json(root / "config" / "resolved.json", resolve_config(root, skill_root))
    append_event(
        root,
        {
            "action": "initialize",
            "object_id": None,
            "object_type": "workspace",
            "reason": "SciPlex workspace initialized",
            "details": {"config_snapshot": "config/resolved.json"},
        },
    )
    return root


def artifact_path(root: Path, object_type: str, filename: str) -> Path:
    if object_type not in OBJECT_TYPES:
        raise ValueError(f"Unknown object type: {object_type}")
    clean_name = Path(filename).name
    return root / "objects" / object_type / clean_name


def validate_workspace(root: Path, require_complete: bool = False) -> Dict[str, Any]:
    issues: List[Dict[str, Any]] = []
    state = load_state(root)

    if not contract_path(root).exists():
        issues.append({"severity": "major", "issue": "Missing .sciplex workspace contract"})
    if not context_path(root).exists():
        issues.append({"severity": "minor", "issue": "Missing context.md workspace brief"})

    if root.exists():
        for entry in root.iterdir():
            if entry.name not in ROOT_ALLOWED_ENTRIES:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Unexpected entry at sciplex root",
                        "path": entry.name,
                        "expected": "Research artifacts belong under objects/<object_type>/",
                    }
                )

    for object_type in OBJECT_TYPES:
        expected = root / "objects" / object_type
        if not expected.exists():
            issues.append({"severity": "major", "issue": "Missing object directory", "path": str(expected.relative_to(root))})

    object_index = state.get("objects", {})

    actual_counts = {object_type: 0 for object_type in OBJECT_TYPES}
    for object_id, meta in object_index.items():
        object_type = meta.get("type")
        if object_type in actual_counts:
            actual_counts[object_type] += 1
            expected_prefix = OBJECT_TYPES[object_type] + "_"
            if not object_id.startswith(expected_prefix):
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Object id prefix does not match object type",
                        "object_id": object_id,
                        "object_type": object_type,
                        "expected_prefix": expected_prefix,
                    }
                )
            object_path_value = meta.get("path")
            if not object_path_value or not (root / object_path_value).exists():
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Indexed object path does not exist",
                        "object_id": object_id,
                        "path": object_path_value,
                    }
                )
            state_value = meta.get("state")
            if state_value not in ALLOWED_STATES.get(object_type, set()):
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Object state is not valid for object type",
                        "object_id": object_id,
                        "object_type": object_type,
                        "state": state_value,
                        "allowed_states": sorted(ALLOWED_STATES.get(object_type, set())),
                    }
                )
    mismatched_counts = {
        object_type: {"state_count": state.get("counts", {}).get(object_type, 0), "actual_count": actual_count}
        for object_type, actual_count in actual_counts.items()
        if state.get("counts", {}).get(object_type, 0) != actual_count
    }
    if mismatched_counts:
        issues.append(
            {
                "severity": "major",
                "issue": "State counts do not match indexed objects",
                "counts": mismatched_counts,
            }
        )

    for object_type in OBJECT_TYPES:
        object_dir = root / "objects" / object_type
        if object_dir.exists() and any(object_dir.iterdir()) and not any(
            meta.get("type") == object_type for meta in object_index.values()
        ):
            issues.append(
                {
                    "severity": "major",
                    "issue": "Artifact directory contains files but has no indexed object",
                    "object_type": object_type,
                    "path": str(object_dir.relative_to(root)),
                }
            )

    indexed_paths = {
        str(Path(meta.get("path", "")).as_posix())
        for meta in object_index.values()
        if meta.get("path")
    }
    indexed_ids = set(object_index)
    unindexed_object_files = []
    invalid_object_like_files = []
    for object_type, prefix in OBJECT_TYPES.items():
        object_dir = root / "objects" / object_type
        if not object_dir.exists():
            continue
        for json_file in object_dir.glob("*.json"):
            rel_path = json_file.relative_to(root).as_posix()
            if rel_path in indexed_paths:
                continue
            candidate_id = json_file.stem
            try:
                candidate_obj = read_json(json_file, {})
            except Exception:
                continue
            embedded_id = candidate_obj.get("id")
            embedded_type = candidate_obj.get("type")
            looks_like_object = bool(embedded_id or embedded_type or re.match(r"^[a-z]+_\d{3,}$", candidate_id))
            if not looks_like_object:
                continue
            if embedded_type and embedded_type != object_type:
                invalid_object_like_files.append(
                    {"path": rel_path, "issue": "embedded type does not match containing object directory"}
                )
            elif embedded_id and embedded_id != candidate_id:
                invalid_object_like_files.append({"path": rel_path, "issue": "embedded id does not match filename"})
            elif candidate_id not in indexed_ids:
                unindexed_object_files.append(rel_path)
    if invalid_object_like_files:
        issues.append(
            {
                "severity": "major",
                "issue": "Object-like JSON files have invalid identity metadata",
                "files": invalid_object_like_files[:20],
            }
        )
    if unindexed_object_files:
        issues.append(
            {
                "severity": "major",
                "issue": "Object-like JSON files under objects/ are not indexed in state.json",
                "files": unindexed_object_files[:20],
                "expected": "Index valid artifacts through the runtime helper, or move scratch/repair files outside objects/.",
            }
        )

    for json_file in root.rglob("*.json"):
        try:
            json.loads(json_file.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001 - validation should report any parse failure.
            issues.append(
                {
                    "severity": "critical",
                    "issue": "Invalid JSON file",
                    "path": str(json_file.relative_to(root)),
                    "error": str(exc),
                }
            )

    events = read_json(events_path(root), {"events": []}).get("events", [])
    object_count = len(state.get("objects", {}))
    create_events = [event for event in events if event.get("action") == "create" and event.get("object_id")]
    if object_count and len(create_events) < object_count:
        issues.append(
            {
                "severity": "major",
                "issue": "Event log does not cover object creation",
                "objects_in_state": object_count,
                "create_events": len(create_events),
            }
        )

    final_output_ids = {
        object_id
        for object_id, meta in object_index.items()
        if meta.get("type") == "paper"
        and read_json(root / meta.get("path", f"objects/paper/{object_id}.json"), {}).get("state") == "final"
    }
    has_final_output = bool(final_output_ids)

    if has_final_output and not any(meta.get("type") == "review" for meta in object_index.values()):
        issues.append(
            {
                "severity": "major",
                "issue": "Final output exists without an indexed review object",
                "expected": "Create a review object or downgrade the output state.",
            }
        )

    if has_final_output and state.get("current_phase") not in {"REVIEWING", "COMPLETE"}:
        issues.append(
            {
                "severity": "major",
                "issue": "Final output inconsistent with workspace phase",
                "current_phase": state.get("current_phase"),
                "expected": "REVIEWING or COMPLETE for final output, otherwise keep output as draft/reviewed.",
            }
        )

    if state.get("current_phase") == "COMPLETE":
        incomplete_orchestrators = [
            object_id
            for object_id, meta in object_index.items()
            if meta.get("type") == "orchestrator" and meta.get("state") != "complete"
        ]
        if incomplete_orchestrators:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Workspace marked COMPLETE with non-complete orchestrator objects",
                    "object_ids": incomplete_orchestrators,
                }
            )
        reviewed_papers = [
            object_id
            for object_id, meta in object_index.items()
            if meta.get("type") == "paper"
            and read_json(root / meta.get("path", f"objects/paper/{object_id}.json"), {}).get("state") == "reviewed"
        ]
        if reviewed_papers:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Workspace marked COMPLETE with reviewed but non-final paper objects",
                    "object_ids": reviewed_papers,
                }
            )

    if state.get("current_phase") == "COMPLETE" and not any(
        meta.get("type") == "console" for meta in object_index.values()
    ):
        issues.append(
            {
                "severity": "major",
                "issue": "Workspace marked COMPLETE without a console object",
                "expected": "Create objects/console/console_data.json and a console object, or downgrade the run status.",
            }
        )

    literature_states = {
        object_id: meta.get("state")
        for object_id, meta in object_index.items()
        if meta.get("type") == "literature"
    }

    if require_complete:
        if state.get("current_phase") != "COMPLETE":
            issues.append(
                {
                    "severity": "major",
                    "issue": "Workspace is not in COMPLETE phase",
                    "current_phase": state.get("current_phase"),
                    "expected": "COMPLETE",
                }
            )
        if not final_output_ids:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Completion-required validation found no final output",
                    "expected": "Finalize the target output or run validation without --require-complete for in-progress audits.",
                }
            )
        required_types = ["orchestrator", "hypothesis", "problem", "data", "method", "finding", "paper", "review", "console"]
        missing_types = [object_type for object_type in required_types if state.get("counts", {}).get(object_type, 0) < 1]
        if missing_types:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Completion-required validation missing required object types",
                    "missing_types": missing_types,
                }
            )
        unresolved_hypotheses = [
            object_id
            for object_id, meta in object_index.items()
            if meta.get("type") == "hypothesis" and meta.get("state") == "formulated"
        ]
        if unresolved_hypotheses:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Completion-required validation has hypotheses that were never tested or assessed",
                    "hypothesis_ids": unresolved_hypotheses,
                    "expected": "Transition hypotheses to tested, supported, refuted, or inconclusive with evidence links before COMPLETE.",
                }
            )
        unvalidated_methods = [
            object_id
            for object_id, meta in object_index.items()
            if meta.get("type") == "method" and meta.get("state") not in {"validated"}
        ]
        if unvalidated_methods:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Completion-required validation has methods that were not validated",
                    "method_ids": unvalidated_methods,
                    "expected": "Validate method fidelity before finalizing the workspace.",
                }
            )

    for object_id, meta in object_index.items():
        if meta.get("type") != "paper":
            continue
        paper_file = root / meta.get("path", f"objects/paper/{object_id}.json")
        paper_obj = read_json(paper_file, {})
        attrs = paper_obj.get("attributes", {})
        if paper_obj.get("state") not in {"reviewed", "final"}:
            continue

        target = attrs.get("output_target", "paper")
        standard = OUTPUT_STANDARDS.get(target)
        if not standard:
            issues.append({"severity": "major", "issue": "Unknown output target", "object_id": object_id, "output_target": target})
            continue

        word_count = int(attrs.get("word_count") or 0)
        citation_ids = attrs.get("citation_ids") or attrs.get("citations") or []
        figure_ids = attrs.get("figure_ids") or attrs.get("figures") or []
        data_ids = attrs.get("data_ids") or attrs.get("data_sources") or attrs.get("source_ids") or []
        if isinstance(data_ids, str):
            data_ids = [data_ids]
        declared_reference_count = attrs.get("reference_count")
        file_path_value = attrs.get("file_path")

        if target == "paper":
            section_plan = attrs.get("section_plan") or attrs.get("sections")
            sections_dir = root / "objects" / "paper" / "sections"
            section_files = list(sections_dir.glob("*.md")) if sections_dir.exists() else []
            if not section_plan and len(section_files) < 4:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Paper target lacks section plan or section draft files",
                        "object_id": object_id,
                        "expected": "Record section_plan/sections or write section drafts under objects/paper/sections/.",
                    }
                )
            missing_link_fields = []
            if not (attrs.get("hypothesis_ids") or attrs.get("hypotheses")):
                missing_link_fields.append("hypothesis_ids")
            if not (attrs.get("data_ids") or attrs.get("data_sources") or attrs.get("source_ids")):
                missing_link_fields.append("data_ids/source_ids")
            if not (attrs.get("method_id") or attrs.get("method_ids")):
                missing_link_fields.append("method_id/method_ids")
            if missing_link_fields:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Paper target lacks core research lineage metadata",
                        "object_id": object_id,
                        "missing_fields": missing_link_fields,
                        "expected": "Record the hypotheses, data/sources, and methods that the paper depends on.",
                    }
                )
            claim_audit = attrs.get("claim_audit") or attrs.get("key_claims")
            weak_claim_audit = []
            if not claim_audit:
                weak_claim_audit.append("missing claim_audit/key_claims")
            elif isinstance(claim_audit, list):
                if len(claim_audit) < 3:
                    weak_claim_audit.append("fewer than 3 audited key claims")
                for idx, claim in enumerate(claim_audit, start=1):
                    if not isinstance(claim, dict):
                        weak_claim_audit.append(f"claim {idx} is not an object")
                        continue
                    if not claim.get("claim"):
                        weak_claim_audit.append(f"claim {idx} lacks claim text")
                    if not any(claim.get(key) for key in ["finding_ids", "source_ids", "literature_ids", "evidence_ids"]):
                        weak_claim_audit.append(f"claim {idx} lacks evidence links")
                    if not claim.get("strength"):
                        weak_claim_audit.append(f"claim {idx} lacks evidence strength")
                    if not (claim.get("limitations") or claim.get("caveats")):
                        weak_claim_audit.append(f"claim {idx} lacks limitations/caveats")
            else:
                weak_claim_audit.append("claim_audit/key_claims is not a list")
            if weak_claim_audit:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Paper target lacks a structured key-claim audit",
                        "object_id": object_id,
                        "problems": weak_claim_audit[:20],
                        "expected": "Record core claims with evidence links, strength, and limitations.",
                    }
                )

        actual_word_count = None
        output_text = ""
        output_regions: Dict[str, Any] = {}
        if not file_path_value:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Final output object lacks file_path",
                    "object_id": object_id,
                }
            )
        elif Path(file_path_value).parts and Path(file_path_value).parts[0] == "sciplex":
            issues.append(
                {
                    "severity": "major",
                    "issue": "Final output file_path should be relative to sciplex root",
                    "object_id": object_id,
                    "file_path": file_path_value,
                    "expected_example": "objects/paper/brief_001.md",
                }
            )
        elif not (root / file_path_value).exists():
            issues.append(
                {
                    "severity": "major",
                    "issue": "Final output file_path does not exist",
                    "object_id": object_id,
                    "file_path": file_path_value,
                }
            )
        else:
            text = (root / file_path_value).read_text(encoding="utf-8", errors="ignore")
            output_text = text
            actual_word_count = count_words(text)
            output_regions = manuscript_regions(text)
            headings = re.findall(r"(?m)^#{1,3}\s+(.+?)\s*$", text)
            duplicate_headings = sorted({heading for heading in headings if headings.count(heading) > 1})
            if duplicate_headings:
                issues.append(
                    {
                        "severity": "minor",
                        "issue": "Output contains duplicate section headings",
                        "object_id": object_id,
                        "headings": duplicate_headings[:12],
                    }
                )
            references_match = re.search(r"(?ims)^(?:#+\s+)?references\s*$([\s\S]+)$", text)
            reference_text = output_regions.get("reference_text") or (references_match.group(1) if references_match else "")
            reference_entries = re.findall(r"(?m)^\s*\d+\.\s+\S+", reference_text)
            if citation_ids and reference_entries and abs(len(reference_entries) - len(citation_ids)) > 2:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Reference list count differs from citation_ids",
                        "object_id": object_id,
                        "reference_entries": len(reference_entries),
                        "citation_ids": len(citation_ids),
                    }
                )
            if target in {"report", "paper", "registered_report"} and reference_text and citation_ids:
                unmatched_titles = []
                unlinked_references = []
                mismatched_reference_links = []
                for lit_id in citation_ids:
                    lit_meta = object_index.get(lit_id)
                    if not lit_meta:
                        continue
                    lit_obj = read_json(root / lit_meta.get("path", f"objects/literature/{lit_id}.json"), {})
                    lit_attrs = lit_obj.get("attributes", {})
                    title = str(lit_attrs.get("title") or "").strip()
                    if title and not has_title_signature(reference_text, title):
                        unmatched_titles.append({"id": lit_id, "title": title})
                    expected_link_tokens = stable_link_tokens(lit_attrs)
                    if expected_link_tokens and title and has_title_signature(reference_text, title):
                        title_words = set(normalize_words(title))
                        reference_lines = [
                            line
                            for line in reference_text.splitlines()
                            if title_words and title_words.issubset(set(normalize_words(line)))
                        ]
                        if reference_lines and not any("http://" in line or "https://" in line for line in reference_lines):
                            unlinked_references.append(lit_id)
                        elif reference_lines and expected_link_tokens:
                            joined_lines = " ".join(reference_lines).lower()
                            if not any(token and token in joined_lines for token in expected_link_tokens):
                                mismatched_reference_links.append(lit_id)
                if unmatched_titles and len(unmatched_titles) > max(2, int(len(citation_ids) * 0.1)):
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Reference section does not match cited literature object titles",
                            "object_id": object_id,
                            "unmatched": unmatched_titles[:12],
                            "expected": "Generate the bibliography from literature object metadata or mark the output as needing citation repair.",
                        }
                    )
                if unlinked_references:
                    severity = "major" if target == "paper" and len(unlinked_references) > max(3, int(len(citation_ids) * 0.15)) else "minor"
                    issues.append(
                        {
                            "severity": severity,
                            "issue": "Reference entries lack clickable external links",
                            "object_id": object_id,
                            "literature_ids": unlinked_references[:20],
                            "expected": "Add DOI, provider page, repository page, or source URL links to bibliography entries where stable identifiers exist.",
                        }
                    )
                if mismatched_reference_links:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Reference entries do not expose the stable identifier recorded in literature objects",
                            "object_id": object_id,
                            "literature_ids": mismatched_reference_links[:20],
                            "expected": "Bibliography links should match DOI/provider/source identifiers stored on cited literature objects.",
                        }
                    )
                body_text = output_regions.get("main_text") or (text[: references_match.start()] if references_match else text)
                unused_citations = []
                for lit_id in citation_ids:
                    lit_meta = object_index.get(lit_id)
                    if not lit_meta:
                        continue
                    lit_obj = read_json(root / lit_meta.get("path", f"objects/literature/{lit_id}.json"), {})
                    lit_attrs = lit_obj.get("attributes", {})
                    if not author_year_mentioned(body_text, lit_attrs):
                        unused_citations.append(lit_id)
                if unused_citations:
                    severity = "major" if len(unused_citations) > max(3, int(len(citation_ids) * 0.15)) else "minor"
                    issues.append(
                        {
                            "severity": severity,
                            "issue": "Reference list includes cited literature objects with no clear in-text use",
                            "object_id": object_id,
                            "literature_ids": unused_citations[:20],
                            "expected": "Use cited sources in the argument or remove them from the final bibliography.",
                        }
                    )
                unlinked_inline_citations = []
                for lit_id in citation_ids:
                    lit_meta = object_index.get(lit_id)
                    if not lit_meta:
                        continue
                    lit_obj = read_json(root / lit_meta.get("path", f"objects/literature/{lit_id}.json"), {})
                    lit_attrs = lit_obj.get("attributes", {})
                    if stable_link_tokens(lit_attrs) and author_year_mentioned(body_text, lit_attrs):
                        if not markdown_linked_author_year(body_text, lit_attrs):
                            unlinked_inline_citations.append(lit_id)
                if unlinked_inline_citations:
                    severity = "major" if target == "paper" and len(unlinked_inline_citations) > max(3, int(len(citation_ids) * 0.15)) else "minor"
                    issues.append(
                        {
                            "severity": severity,
                            "issue": "In-text cited sources are not linked at substantive mention",
                            "object_id": object_id,
                            "literature_ids": unlinked_inline_citations[:20],
                            "expected": "Use Markdown links such as [Author (Year)](DOI/provider URL) at first substantive mention.",
                        }
                    )
            if actual_word_count and word_count and abs(actual_word_count - word_count) > max(250, int(word_count * 0.2)):
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Declared word_count differs substantially from output file",
                        "object_id": object_id,
                        "declared_word_count": word_count,
                        "actual_word_count": actual_word_count,
                    }
                )
            declared_actual = attrs.get("word_count_actual")
            if declared_actual is not None and abs(int(declared_actual) - actual_word_count) > max(250, int(actual_word_count * 0.1)):
                issues.append(
                    {
                        "severity": "major",
                        "issue": "word_count_actual metadata differs substantially from output file",
                        "object_id": object_id,
                        "declared_word_count_actual": int(declared_actual),
                        "actual_word_count": actual_word_count,
                    }
                )
            if target in {"report", "paper"}:
                main_text = output_regions.get("main_text") or (text[: references_match.start()] if references_match else text)
                appendix_match = re.search(r"(?im)^##\s+appendix\b", main_text)
                pre_appendix_text = main_text[: appendix_match.start()] if appendix_match else main_text
                internal_paths = sorted(
                    set(re.findall(r"`?(objects/(?:data|literature|method|experiment|paper|console|review|failed)/[^`)\s,;]+)`?", pre_appendix_text))
                )
                if internal_paths:
                    issues.append(
                        {
                            "severity": "major" if target == "paper" else "minor",
                            "issue": "Main prose exposes internal SciPlex artifact paths",
                            "object_id": object_id,
                            "paths": internal_paths[:12],
                            "expected": "Use public source names and URLs in the manuscript body; reserve internal object paths for reproducibility appendices.",
                        }
                    )
                mechanical_phrases = [
                    "is used as contextual literature on",
                    "helps locate this analysis in broader",
                    "is used here as contextual literature",
                ]
                found_mechanical = [phrase for phrase in mechanical_phrases if phrase in text.lower()]
                if found_mechanical:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Output contains mechanical citation inventory prose",
                            "object_id": object_id,
                            "phrases": found_mechanical,
                            "expected": "Synthesize cited sources into the argument instead of listing why each citation is used.",
                        }
                    )
                paragraphs = [
                    re.sub(r"\s+", " ", paragraph.strip().lower())
                    for paragraph in re.split(r"\n\s*\n", text)
                    if len(paragraph.split()) >= 30
                ]
                repeated = sorted({paragraph for paragraph in paragraphs if paragraphs.count(paragraph) > 2})
                if repeated:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Output appears padded with repeated paragraphs",
                            "object_id": object_id,
                            "repeat_count": max(paragraphs.count(paragraph) for paragraph in repeated),
                            "example": repeated[0][:240],
                            "expected": "Expand with new evidence, robustness checks, limitations, or interpretation instead of repeated prose.",
                        }
                    )
            if target == "paper":
                main_word_count = int(output_regions.get("main_word_count") or 0)
                appendix_word_count = int(output_regions.get("appendix_word_count") or 0)
                section_counts = paper_section_word_counts(output_regions.get("sections") or [])
                short_sections = {
                    section: {"word_count": count, "minimum": PAPER_SECTION_MIN_WORDS[section]}
                    for section, count in section_counts.items()
                    if count < PAPER_SECTION_MIN_WORDS[section]
                }
                if short_sections:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Paper target has underdeveloped core sections",
                            "object_id": object_id,
                            "sections": short_sections,
                            "expected": "Draft each journal-paper section substantively; references and appendices cannot compensate for thin Introduction, Methods, Results, or Discussion.",
                        }
                    )
                ordered_numbers = numbered_section_order_problem(output_regions.get("sections") or [])
                if ordered_numbers:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Paper section numbering is out of order",
                            "object_id": object_id,
                            "section_numbers": ordered_numbers,
                            "expected": "Assemble the manuscript in reader order before marking it reviewed or final.",
                        }
                    )
                appendix_ratio = appendix_word_count / max(main_word_count, 1)
                robustness_note_count = len(re.findall(r"(?i)\brobustness note\s+\d+\b", output_regions.get("appendix_text") or output_text))
                if appendix_ratio > 0.35:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Paper relies too heavily on appendices relative to main text",
                            "object_id": object_id,
                            "main_text_word_count": main_word_count,
                            "appendix_word_count": appendix_word_count,
                            "expected": "Use appendices for reproducibility artifacts, supplemental tables, or sensitivity details; they do not count toward the journal-paper body.",
                        }
                    )
                if robustness_note_count > 5:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Appendix or robustness material appears padded with enumerated notes",
                            "object_id": object_id,
                            "robustness_note_count": robustness_note_count,
                            "expected": "Replace generic note accumulation with real robustness analyses, tables, code outputs, or concise limitations.",
                        }
                    )
            if target in {"report", "paper"}:
                malformed_tables = []
                lines = text.splitlines()
                idx = 0
                separator_pattern = re.compile(r"\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$")
                while idx < len(lines):
                    line = lines[idx]
                    if "|" not in line or line.count("|") < 2:
                        idx += 1
                        continue
                    start = idx
                    while idx < len(lines) and "|" in lines[idx] and lines[idx].count("|") >= 2:
                        idx += 1
                    block = lines[start:idx]
                    has_separator = len(block) >= 2 and any(separator_pattern.match(block[pos]) for pos in range(1, min(3, len(block))))
                    if not has_separator:
                        malformed_tables.append({"line": start + 1, "text": block[0][:160]})
                if malformed_tables:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Output contains pipe-delimited table text that is not a valid Markdown table",
                            "object_id": object_id,
                            "examples": malformed_tables[:8],
                            "expected": "Add a Markdown separator row such as |---|---| after table headers, or link a separate table file.",
                        }
                    )

        effective_word_count = actual_word_count if actual_word_count is not None else word_count
        if target == "paper" and output_regions:
            effective_word_count = int(output_regions.get("main_word_count") or 0)
        if effective_word_count < standard["min_words"]:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Output below target word-count standard",
                    "object_id": object_id,
                    "output_target": target,
                    "count_basis": standard.get("count_basis", "full_output"),
                    "word_count": effective_word_count,
                    "minimum": standard["min_words"],
                }
            )
        if standard.get("max_words") and effective_word_count > standard["max_words"]:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Output above target word-count standard",
                    "object_id": object_id,
                    "output_target": target,
                    "word_count": effective_word_count,
                    "maximum": standard["max_words"],
                }
            )
        if len(citation_ids) < standard["min_references"]:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Output below target reference standard",
                    "object_id": object_id,
                    "output_target": target,
                    "references": len(citation_ids),
                    "minimum": standard["min_references"],
                }
            )
        if len(figure_ids) < standard["min_figures"]:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Output below target figure/table standard",
                    "object_id": object_id,
                    "output_target": target,
                    "figures": len(figure_ids),
                    "minimum": standard["min_figures"],
                }
            )
        missing_figures = []
        figure_paths = []
        for figure_id in figure_ids:
            figure_meta = object_index.get(figure_id)
            if not figure_meta:
                missing_figures.append({"id": figure_id, "issue": "not indexed"})
                continue
            figure_obj = read_json(root / figure_meta.get("path", f"objects/figure/{figure_id}.json"), {})
            figure_attrs = figure_obj.get("attributes", {})
            if figure_obj.get("state") == "finalized" and figure_attrs.get("needs_generation") is True:
                missing_figures.append({"id": figure_id, "issue": "finalized figure still marked needs_generation"})
            if figure_obj.get("state") == "finalized":
                figure_type = str(figure_attrs.get("figure_type") or "").lower()
                has_sources = bool(figure_attrs.get("evidence_sources") or figure_attrs.get("literature_ids") or figure_attrs.get("data_ids"))
                has_encoding = any(
                    figure_attrs.get(key)
                    for key in [
                        "data_points",
                        "data_values",
                        "statistics",
                        "table_rows",
                        "visual_encoding",
                        "diagram_elements",
                    ]
                )
                if not has_sources:
                    missing_figures.append({"id": figure_id, "issue": "finalized figure lacks evidence_sources/literature_ids/data_ids"})
                if figure_type not in {"conceptual_diagram", "schema", "workflow"} and not has_encoding:
                    missing_figures.append({"id": figure_id, "issue": "finalized data figure/table lacks data_points/statistics/visual_encoding metadata"})
                if figure_type not in {"table", "data_table"} and not (
                    figure_attrs.get("style_profile") or figure_attrs.get("visual_style") or figure_attrs.get("design_notes")
                ):
                    missing_figures.append({"id": figure_id, "issue": "finalized figure lacks visual style metadata"})
            figure_path_value = figure_attrs.get("file_path") or figure_attrs.get("path")
            if not figure_path_value:
                missing_figures.append({"id": figure_id, "issue": "missing file_path"})
            elif Path(figure_path_value).parts and Path(figure_path_value).parts[0] == "sciplex":
                missing_figures.append({"id": figure_id, "issue": "file_path should be relative to sciplex root"})
            elif not (root / figure_path_value).exists():
                missing_figures.append({"id": figure_id, "issue": "file_path does not exist", "file_path": figure_path_value})
            else:
                figure_file = root / figure_path_value
                figure_paths.append(str(figure_path_value).replace("\\", "/"))
                suffix = figure_file.suffix.lower()
                try:
                    header = figure_file.read_bytes()[:32]
                    if suffix == ".png" and not header.startswith(b"\x89PNG\r\n\x1a\n"):
                        missing_figures.append({"id": figure_id, "issue": "png file is not a valid PNG image", "file_path": figure_path_value})
                    elif suffix in {".jpg", ".jpeg"} and not header.startswith(b"\xff\xd8\xff"):
                        missing_figures.append({"id": figure_id, "issue": "jpeg file is not a valid JPEG image", "file_path": figure_path_value})
                    elif suffix == ".gif" and not header.startswith((b"GIF87a", b"GIF89a")):
                        missing_figures.append({"id": figure_id, "issue": "gif file is not a valid GIF image", "file_path": figure_path_value})
                    elif suffix == ".webp" and not (header.startswith(b"RIFF") and b"WEBP" in header[:16]):
                        missing_figures.append({"id": figure_id, "issue": "webp file is not a valid WebP image", "file_path": figure_path_value})
                    elif suffix == ".svg":
                        svg_head = figure_file.read_text(encoding="utf-8", errors="ignore")[:200].lower()
                        if "<svg" not in svg_head:
                            missing_figures.append({"id": figure_id, "issue": "svg file does not contain an svg element", "file_path": figure_path_value})
                    if suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}:
                        probe_text = figure_file.read_text(encoding="utf-8", errors="ignore")[:500].lower()
                        if "placeholder" in probe_text or "needs generation" in probe_text:
                            missing_figures.append({"id": figure_id, "issue": "figure file appears to be a placeholder", "file_path": figure_path_value})
                except Exception as exc:  # noqa: BLE001 - validation should report unreadable artifacts.
                    missing_figures.append({"id": figure_id, "issue": "figure file could not be validated", "file_path": figure_path_value, "error": str(exc)})
        if missing_figures:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Final output references figure objects without valid files",
                    "object_id": object_id,
                    "figures": missing_figures,
                }
            )
        if target in {"report", "paper"} and output_text and figure_paths:
            normalized_output_text = output_text.replace("\\", "/")
            markdown_linked_figures = []
            raw_only_figures = []
            unembedded_figures = [
                figure_path
                for figure_path in figure_paths
                if figure_path not in normalized_output_text
            ]
            for figure_path in figure_paths:
                path_pattern = re.escape(figure_path)
                image_link = re.search(r"!\[[^\]]*\]\(\s*<?" + path_pattern + r">?(?:\s+\"[^\"]*\")?\s*\)", normalized_output_text)
                text_link = re.search(r"(?<!!)\[[^\]]+\]\(\s*<?" + path_pattern + r">?(?:\s+\"[^\"]*\")?\s*\)", normalized_output_text)
                if image_link or text_link:
                    markdown_linked_figures.append(figure_path)
                elif figure_path in normalized_output_text:
                    raw_only_figures.append(figure_path)
            if unembedded_figures:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Final output does not embed or link referenced figure files",
                        "object_id": object_id,
                        "figure_files": unembedded_figures[:12],
                        "expected": "Embed or link each main figure/table file in the manuscript body.",
                    }
                )
            if raw_only_figures:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Final output mentions figure files without Markdown image/link syntax",
                        "object_id": object_id,
                        "figure_files": raw_only_figures[:12],
                        "expected": "Use ![caption](objects/figure/file.png) for images or [Table N](objects/figure/file.md) for table files.",
                    }
                )
        if target in {"report", "paper"} and output_text and data_ids:
            normalized_output_text = output_text.replace("\\", "/")
            unlinked_data_sources = []
            for data_id in data_ids:
                data_meta = object_index.get(data_id)
                if not data_meta:
                    continue
                data_obj = read_json(root / data_meta.get("path", f"objects/data/{data_id}.json"), {})
                data_attrs = data_obj.get("attributes", {})
                public_links = [
                    str(data_attrs.get(key) or "").strip()
                    for key in ["source_url", "url", "landing_page_url", "repository_url", "api_url"]
                    if data_attrs.get(key)
                ]
                if public_links and not any(link in normalized_output_text for link in public_links):
                    unlinked_data_sources.append(data_id)
            if unlinked_data_sources:
                issues.append(
                    {
                        "severity": "major" if target == "paper" else "minor",
                        "issue": "Final output does not expose clickable source links for cited data objects",
                        "object_id": object_id,
                        "data_ids": unlinked_data_sources,
                        "expected": "Link public dataset landing pages or source URLs in the methods/data section.",
                    }
                )
        source_roles = set()
        weak_relevance_lit = []
        for lit_id in citation_ids:
            lit_meta = object_index.get(lit_id)
            if not lit_meta:
                continue
            lit_obj = read_json(root / lit_meta.get("path", f"objects/literature/{lit_id}.json"), {})
            lit_attrs = lit_obj.get("attributes", {})
            role = lit_attrs.get("source_role") or lit_attrs.get("evidence_role") or lit_attrs.get("source_type")
            if role:
                source_roles.add(str(role))
            if target == "paper":
                relevance_fields = [
                    lit_attrs.get("relevance_assessment"),
                    lit_attrs.get("inclusion_reason"),
                    lit_attrs.get("selection_reason"),
                    lit_attrs.get("relevance_to_question"),
                    lit_attrs.get("evidence_role"),
                    lit_attrs.get("source_role"),
                ]
                if not any(str(value or "").strip() for value in relevance_fields):
                    weak_relevance_lit.append(lit_id)
        if weak_relevance_lit:
            issues.append(
                {
                    "severity": "major" if len(weak_relevance_lit) > max(3, int(len(citation_ids) * 0.2)) else "minor",
                    "issue": "Paper cites literature without explicit relevance or inclusion rationale",
                    "object_id": object_id,
                    "literature_ids": weak_relevance_lit[:30],
                    "expected": "Curate cited literature objects with source_role/evidence_role and a short relevance_assessment or inclusion_reason before using them in a paper.",
                }
            )
        declared_coverage = attrs.get("source_coverage") or attrs.get("coverage")
        if len(source_roles) < standard["min_source_roles"] and not declared_coverage:
            issues.append(
                {
                    "severity": "major" if target in {"report", "paper", "registered_report"} else "minor",
                    "issue": "Output lacks sufficient source-role coverage",
                    "object_id": object_id,
                    "output_target": target,
                    "source_roles": sorted(source_roles),
                    "minimum": standard["min_source_roles"],
                    "expected": "Add source_role/evidence_role to cited literature or record source_coverage in the output object.",
                }
            )
        if declared_reference_count is not None and int(declared_reference_count) != len(citation_ids):
            issues.append(
                {
                    "severity": "minor",
                    "issue": "Declared reference_count differs from citation list length",
                    "object_id": object_id,
                    "reference_count": int(declared_reference_count),
                    "citations": len(citation_ids),
                }
            )

        unresolved_lit = [
            lit_id
            for lit_id in citation_ids
            if literature_states.get(lit_id) not in {"read", "cited", "validated"}
        ]
        if unresolved_lit:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Final output cites literature that was not read/cited/validated",
                    "object_id": object_id,
                    "literature_ids": unresolved_lit,
                }
            )
        if paper_obj.get("state") == "final" and target in {"report", "paper", "registered_report"}:
            merely_read_lit = [
                lit_id
                for lit_id in citation_ids
                if literature_states.get(lit_id) == "read"
            ]
            if merely_read_lit:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Final output cites literature that is read but not marked cited/validated",
                        "object_id": object_id,
                        "literature_ids": merely_read_lit[:40],
                        "expected": "Transition cited literature to cited or validated before final output.",
                    }
                )

        weak_bibliography = []
        for lit_id in citation_ids:
            lit_meta = object_index.get(lit_id)
            if not lit_meta:
                continue
            lit_obj = read_json(root / lit_meta.get("path", f"objects/literature/{lit_id}.json"), {})
            lit_attrs = lit_obj.get("attributes", {})
            has_identifier = any(
                lit_attrs.get(key)
                for key in ["doi", "url", "source_url", "openalex_id", "arxiv_id", "pmid", "nber_id", "isbn"]
            )
            if not has_identifier and lit_attrs.get("needs_verification") is not True:
                weak_bibliography.append(lit_id)
        if weak_bibliography:
            issues.append(
                {
                    "severity": "minor",
                    "issue": "Cited literature lacks stable identifier and is not marked needs_verification",
                    "literature_ids": weak_bibliography,
                }
            )

        finding_ids = attrs.get("finding_ids") or attrs.get("findings") or []
        weak_findings = []
        for finding_id in finding_ids:
            finding_meta = object_index.get(finding_id)
            if not finding_meta:
                weak_findings.append(finding_id)
                continue
            finding_obj = read_json(root / finding_meta.get("path", f"objects/finding/{finding_id}.json"), {})
            finding_attrs = finding_obj.get("attributes", {})
            has_chain = any(
                finding_attrs.get(key)
                for key in ["evidence_chain", "experiment_ids", "method_ids", "data_ids", "literature_ids"]
            )
            if not has_chain:
                weak_findings.append(finding_id)
        if weak_findings:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Final output references findings without explicit evidence chains",
                    "object_id": object_id,
                    "finding_ids": weak_findings,
                }
            )

    for object_id, meta in object_index.items():
        if meta.get("type") != "experiment":
            continue
        exp_file = root / meta.get("path", f"objects/experiment/{object_id}.json")
        exp_obj = read_json(exp_file, {})
        if exp_obj.get("state") != "completed":
            continue
        exp_attrs = exp_obj.get("attributes", {})
        if not exp_attrs.get("evidence_mode"):
            issues.append(
                {
                    "severity": "major",
                    "issue": "Completed experiment lacks evidence_mode",
                    "object_id": object_id,
                }
            )
        if not any(exp_attrs.get(key) for key in ["data_id", "data_ids", "literature_ids", "source_ids", "input_files"]):
            issues.append(
                {
                    "severity": "major",
                    "issue": "Completed experiment lacks data/source inputs",
                    "object_id": object_id,
                }
            )

    blocking_issues = [issue for issue in issues if issue.get("severity") in {"critical", "major"}]

    for object_id, meta in object_index.items():
        if meta.get("type") != "review":
            continue
        review_obj = read_json(root / meta.get("path", f"objects/review/{object_id}.json"), {})
        review_attrs = review_obj.get("attributes", {})
        target_object = review_attrs.get("target_object") or review_attrs.get("target_id")
        if target_object in final_output_ids:
            dimensions = review_attrs.get("dimensions") or review_attrs.get("review_dimensions") or {}
            covered_dimensions = set(dimensions) if isinstance(dimensions, dict) else set(dimensions or [])
            missing_dimensions = sorted(REVIEW_DIMENSIONS - covered_dimensions)
            if missing_dimensions:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Final output review lacks mandatory review dimensions",
                        "object_id": object_id,
                        "target_object": target_object,
                        "missing_dimensions": missing_dimensions,
                        "expected": "Review method fidelity, evidence chains, claim validity, source coverage, output standards, limitations, and overclaim risk.",
                    }
                )
            if isinstance(dimensions, dict):
                empty_dimensions = [
                    name
                    for name in REVIEW_DIMENSIONS & covered_dimensions
                    if not dimensions.get(name)
                ]
                if empty_dimensions:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Final output review has empty mandatory dimensions",
                            "object_id": object_id,
                            "dimensions": empty_dimensions,
                        }
                    )
        review_claims_pass = (
            review_attrs.get("passed") is True
            or str(review_attrs.get("recommendation", "")).lower() in {"accept", "pass", "passed"}
            or str((review_attrs.get("results") or {}).get("status", "")).lower() in {"pass", "passed"}
        )
        if review_claims_pass and blocking_issues:
            issues.append(
                {
                    "severity": "major",
                    "issue": "Review object claims pass despite blocking validator issues",
                    "object_id": object_id,
                    "blocking_issue_count": len(blocking_issues),
                }
            )

    for object_id, meta in object_index.items():
        if meta.get("type") != "console":
            continue
        console_obj = read_json(root / meta.get("path", f"objects/console/{object_id}.json"), {})
        console_attrs = console_obj.get("attributes", {})
        console_data_path = console_attrs.get("console_data_path")
        if console_data_path and (root / console_data_path).exists():
            console_data = read_json(root / console_data_path, {})
            validator_result = console_data.get("validator_result") or {}
            status = str(validator_result.get("status", "")).lower()
            if status in {"pass", "passed"} and blocking_issues:
                issues.append(
                    {
                        "severity": "major",
                        "issue": "Console validator_result claims pass despite blocking validator issues",
                        "object_id": object_id,
                        "blocking_issue_count": len(blocking_issues),
                    }
                )
            if require_complete:
                validator_issues = validator_result.get("issues")
                if status in {"pass", "passed"} and validator_issues:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Console validator_result is stale or internally inconsistent",
                            "object_id": object_id,
                            "expected": "A passing final console validator_result must not retain old issues.",
                        }
                    )
                console_counts = console_data.get("object_counts") or {}
                mismatched_console_counts = {
                    object_type: {"console_count": console_counts.get(object_type, 0), "state_count": state.get("counts", {}).get(object_type, 0)}
                    for object_type in OBJECT_TYPES
                    if console_counts.get(object_type, 0) != state.get("counts", {}).get(object_type, 0)
                }
                if mismatched_console_counts:
                    issues.append(
                        {
                            "severity": "major",
                            "issue": "Console object_counts do not match state.json",
                            "object_id": object_id,
                            "counts": mismatched_console_counts,
                        }
                    )
                final_output = console_data.get("final_output") or {}
                final_paper_id = final_output.get("paper_id")
                if final_paper_id and final_paper_id in object_index:
                    paper_meta = object_index[final_paper_id]
                    paper_obj = read_json(root / paper_meta.get("path", f"objects/paper/{final_paper_id}.json"), {})
                    paper_attrs = paper_obj.get("attributes", {})
                    paper_path_value = paper_attrs.get("file_path")
                    if paper_path_value and (root / paper_path_value).exists():
                        paper_text = (root / paper_path_value).read_text(encoding="utf-8", errors="ignore")
                        actual_words = len(re.findall(r"\b[\w'-]+\b", paper_text))
                        if final_output.get("word_count_actual") and abs(int(final_output["word_count_actual"]) - actual_words) > max(250, int(actual_words * 0.1)):
                            issues.append(
                                {
                                    "severity": "major",
                                    "issue": "Console final_output word count is stale",
                                    "object_id": object_id,
                                    "console_word_count": int(final_output["word_count_actual"]),
                                    "actual_word_count": actual_words,
                                }
                            )

    return {
        "status": "pass" if not any(i["severity"] in {"critical", "major"} for i in issues) else "fail",
        "issues": issues,
    }


def next_object_id(state: Dict[str, Any], object_type: str) -> str:
    prefix = OBJECT_TYPES[object_type]
    existing = state.get("objects", {})
    max_n = 0
    for object_id, meta in existing.items():
        if meta.get("type") != object_type or not object_id.startswith(prefix + "_"):
            continue
        suffix = object_id.rsplit("_", 1)[-1]
        if suffix.isdigit():
            max_n = max(max_n, int(suffix))
    return f"{prefix}_{max_n + 1:03d}"


def object_file(root: Path, object_type: str, object_id: str) -> Path:
    return root / "objects" / object_type / f"{object_id}.json"


def parse_json_arg(value: str) -> Dict[str, Any]:
    path = Path(value)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8-sig"))
    return json.loads(value)


def create_object(
    root: Path,
    object_type: str,
    state_value: str,
    attributes: Dict[str, Any],
    reason: str,
    object_id: str | None = None,
) -> Dict[str, Any]:
    if object_type not in OBJECT_TYPES:
        raise ValueError(f"Unknown object type: {object_type}")

    state = load_state(root)
    object_id = object_id or next_object_id(state, object_type)
    expected_prefix = OBJECT_TYPES[object_type] + "_"
    if not object_id.startswith(expected_prefix):
        raise ValueError(f"Object id {object_id!r} must start with {expected_prefix!r} for type {object_type!r}")
    path = object_file(root, object_type, object_id)
    if path.exists():
        raise FileExistsError(f"Object already exists: {object_id}")

    obj = {
        "id": object_id,
        "type": object_type,
        "state": state_value,
        "attributes": attributes,
    }
    write_json(path, obj)

    state["objects"][object_id] = {"type": object_type, "state": state_value, "path": str(path.relative_to(root))}
    state["counts"][object_type] = state["counts"].get(object_type, 0) + 1
    save_state(root, state)
    append_event(
        root,
        {
            "action": "create",
            "object_id": object_id,
            "object_type": object_type,
            "state_after": state_value,
            "reason": reason,
            "details": {"path": str(path.relative_to(root))},
        },
    )
    return obj


def transition_object(root: Path, object_id: str, new_state: str, reason: str, phase: str | None = None) -> Dict[str, Any]:
    state = load_state(root)
    meta = state["objects"].get(object_id)
    if not meta:
        raise KeyError(f"Object not found in state index: {object_id}")

    object_type = meta["type"]
    path = root / meta.get("path", f"objects/{object_type}/{object_id}.json")
    obj = read_json(path, {})
    before = obj.get("state", meta.get("state"))
    obj["state"] = new_state
    write_json(path, obj)

    meta["state"] = new_state
    if phase:
        state["current_phase"] = phase
    save_state(root, state)
    append_event(
        root,
        {
            "action": "transition",
            "object_id": object_id,
            "object_type": object_type,
            "state_before": before,
            "state_after": new_state,
            "reason": reason,
            "details": {"phase": phase} if phase else {},
        },
    )
    return obj


def remove_object(root: Path, object_id: str, reason: str) -> Dict[str, Any]:
    state = load_state(root)
    meta = state["objects"].get(object_id)
    if not meta:
        raise KeyError(f"Object not found in state index: {object_id}")

    removed = state["objects"].pop(object_id)
    object_type = removed.get("type")
    if object_type in state.get("counts", {}):
        state["counts"][object_type] = max(0, state["counts"].get(object_type, 0) - 1)
    save_state(root, state)
    append_event(
        root,
        {
            "action": "remove",
            "object_id": object_id,
            "object_type": object_type,
            "state_before": removed.get("state"),
            "reason": reason,
            "details": {
                "path": removed.get("path"),
                "note": "Object removed from state index only; file retained for audit.",
            },
        },
    )
    return removed


def validate_phase_transition(current: str, target: str) -> List[str]:
    """Return warnings, not hard failures. Agent remains responsible for judgment."""
    if target in SPECIAL_PHASES or current in SPECIAL_PHASES:
        return []
    if current not in FORWARD_PHASES or target not in FORWARD_PHASES:
        return [f"Unknown phase transition: {current} -> {target}"]
    if FORWARD_PHASES.index(target) < FORWARD_PHASES.index(current):
        return [f"Backward phase transition should be justified: {current} -> {target}"]
    return []


def set_phase(root: Path, target: str, reason: str) -> Dict[str, Any]:
    state = load_state(root)
    current = state.get("current_phase", "IDLE")
    warnings = validate_phase_transition(current, target)
    state["current_phase"] = target
    save_state(root, state)
    append_event(
        root,
        {
            "action": "transition",
            "object_id": None,
            "object_type": "workspace",
            "state_before": current,
            "state_after": target,
            "reason": reason,
            "details": {"warnings": warnings},
        },
    )
    return {"current_phase": target, "warnings": warnings}


def main() -> None:
    parser = argparse.ArgumentParser(description="SciPlex deterministic runtime helper")
    parser.add_argument("--workspace", default=".", help="Workspace root or sciplex/ directory")
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[1]))
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Create workspace layout and config snapshot")
    sub.add_parser("resolve-config", help="Refresh redacted resolved config snapshot")
    validate = sub.add_parser("validate-workspace", help="Validate workspace contract, paths, JSON, and event coverage")
    validate.add_argument(
        "--require-complete",
        action="store_true",
        help="Also require COMPLETE phase, a final output, review, console, and core study object types.",
    )

    path_cmd = sub.add_parser("artifact-path", help="Return canonical path for an artifact under objects/<type>/")
    path_cmd.add_argument("--type", required=True, choices=sorted(OBJECT_TYPES))
    path_cmd.add_argument("--filename", required=True)

    create = sub.add_parser("create-object", help="Create an object and update state/events")
    create.add_argument("--type", required=True, choices=sorted(OBJECT_TYPES))
    create.add_argument("--state", required=True)
    create.add_argument("--attributes", default="{}", help="JSON string or path to JSON file")
    create.add_argument("--id")
    create.add_argument("--reason", required=True)

    transition = sub.add_parser("transition-object", help="Transition an existing object")
    transition.add_argument("--id", required=True)
    transition.add_argument("--state", required=True)
    transition.add_argument("--reason", required=True)
    transition.add_argument("--phase")

    remove = sub.add_parser("remove-object", help="Remove an object from state index while retaining its file for audit")
    remove.add_argument("--id", required=True)
    remove.add_argument("--reason", required=True)

    phase = sub.add_parser("set-phase", help="Set workspace phase and log transition")
    phase.add_argument("--phase", required=True)
    phase.add_argument("--reason", required=True)

    event = sub.add_parser("event", help="Append an arbitrary audit event")
    event.add_argument("--action", required=True)
    event.add_argument("--reason", required=True)
    event.add_argument("--object-id")
    event.add_argument("--object-type", default="workspace")
    event.add_argument("--details", default="{}", help="JSON string or path to JSON file")

    args = parser.parse_args()
    root = sciplex_root(Path(args.workspace))
    skill_root = Path(args.skill_root).resolve()

    if args.command == "init":
        root = initialize_workspace(Path(args.workspace), skill_root)
        print(json.dumps({"status": "initialized", "workspace": str(root)}, indent=2))
    elif args.command == "resolve-config":
        write_json(root / "config" / "resolved.json", resolve_config(root, skill_root))
        print(json.dumps({"status": "resolved", "path": str(root / "config" / "resolved.json")}, indent=2))
    elif args.command == "validate-workspace":
        print(json.dumps(validate_workspace(root, require_complete=args.require_complete), indent=2))
    elif args.command == "artifact-path":
        print(str(artifact_path(root, args.type, args.filename)))
    elif args.command == "create-object":
        obj = create_object(root, args.type, args.state, parse_json_arg(args.attributes), args.reason, args.id)
        print(json.dumps(obj, indent=2))
    elif args.command == "transition-object":
        obj = transition_object(root, args.id, args.state, args.reason, args.phase)
        print(json.dumps(obj, indent=2))
    elif args.command == "remove-object":
        obj = remove_object(root, args.id, args.reason)
        print(json.dumps(obj, indent=2))
    elif args.command == "set-phase":
        result = set_phase(root, args.phase, args.reason)
        print(json.dumps(result, indent=2))
    elif args.command == "event":
        result = append_event(
            root,
            {
                "action": args.action,
                "object_id": args.object_id,
                "object_type": args.object_type,
                "reason": args.reason,
                "details": parse_json_arg(args.details),
            },
        )
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
