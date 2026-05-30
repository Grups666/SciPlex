"""
Compatibility wrapper for initializing a SciPlex workspace.

Prefer `scripts/sciplex_runtime.py init` for new automation. This wrapper keeps
the older documented command working while delegating to the runtime helper.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from sciplex_runtime import initialize_workspace


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a SciPlex workspace")
    parser.add_argument("--workspace", default=".", help="Workspace root where sciplex/ will be created")
    parser.add_argument(
        "--skill-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="SciPlex skill root containing skill-level config/",
    )
    args = parser.parse_args()

    root = initialize_workspace(Path(args.workspace).resolve(), Path(args.skill_root).resolve())
    print(json.dumps({"status": "initialized", "workspace": str(root)}, indent=2))


if __name__ == "__main__":
    main()
