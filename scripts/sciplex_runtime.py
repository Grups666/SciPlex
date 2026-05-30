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
    elif args.command == "create-object":
        obj = create_object(root, args.type, args.state, parse_json_arg(args.attributes), args.reason, args.id)
        print(json.dumps(obj, indent=2))
    elif args.command == "transition-object":
        obj = transition_object(root, args.id, args.state, args.reason, args.phase)
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
