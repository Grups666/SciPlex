"""
execute_analysis.py - Deterministic analysis execution for SciPlex

Purpose: Execute analytical methods reproducibly. LLM decides what to run;
         this script handles deterministic execution, logging, and error handling.

Usage:
    python execute_analysis.py --method <method_id> --data <data_id> --config <config.json>

This script is called by the SciPlex skill when:
- Method has been implemented (meth_XXX.py exists)
- Data has been validated (data_XXX.json with file_path)
- LLM has decided to run this specific experiment
"""

import argparse
import json
import sys
import subprocess
import traceback
from pathlib import Path
from datetime import datetime

from sciplex_runtime import append_event, load_state, save_state

def load_method(method_path: Path):
    """Load method definition from JSON"""
    with open(method_path) as f:
        return json.load(f)

def load_data(data_path: Path):
    """Load data definition from JSON"""
    with open(data_path) as f:
        return json.load(f)

def execute(method_id: str, data_id: str, config: dict, workspace: Path):
    """
    Execute analysis method on data with given configuration.

    Returns: dict with outputs, status, lessons
    """
    # Resolve paths
    method_json = workspace / "objects" / "method" / f"{method_id}.json"
    method_code = workspace / "objects" / "method" / f"{method_id}.py"
    data_json = workspace / "objects" / "data" / f"{data_id}.json"

    # Check existence
    if not method_json.exists():
        return {"status": "failed", "lessons": f"Method {method_id} not found"}
    if not method_code.exists():
        return {"status": "failed", "lessons": f"Method code {method_id}.py not found"}
    if not data_json.exists():
        return {"status": "failed", "lessons": f"Data {data_id} not found"}

    # Load definitions
    method = load_method(method_json)
    data = load_data(data_json)

    # Prepare output directory
    exp_id = f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir = workspace / "objects" / "experiment" / exp_id
    output_dir.mkdir(parents=True, exist_ok=True)

    # Execute method code
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(method_code),
                "--data", str(data["attributes"]["file_path"]),
                "--output", str(output_dir),
                "--config", json.dumps(config)
            ],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            # Success - record outputs
            outputs = list(output_dir.glob("*"))
            return {
                "status": "completed",
                "outputs": [str(p) for p in outputs],
                "log": result.stdout,
                "exp_id": exp_id
            }
        else:
            # Failure - record lessons
            return {
                "status": "failed",
                "lessons": result.stderr or "Unknown error",
                "exp_id": exp_id
            }

    except subprocess.TimeoutExpired:
        return {
            "status": "failed",
            "lessons": "Execution timeout (>5min)",
            "exp_id": exp_id
        }
    except Exception as e:
        return {
            "status": "failed",
            "lessons": f"Execution error: {str(e)}",
            "exp_id": exp_id
        }

def main():
    parser = argparse.ArgumentParser(description="Execute SciPlex analysis")
    parser.add_argument("--method", required=True, help="Method ID (e.g., meth_001)")
    parser.add_argument("--data", required=True, help="Data ID (e.g., data_001)")
    parser.add_argument("--config", required=True, help="Config JSON string or path")
    parser.add_argument("--workspace", default="sciplex", help="Workspace path")

    args = parser.parse_args()

    # Parse config
    if Path(args.config).exists():
        with open(args.config) as f:
            config = json.load(f)
    else:
        config = json.loads(args.config)

    workspace = Path(args.workspace)

    # Execute
    result = execute(args.method, args.data, config, workspace)

    # Output result
    print(json.dumps(result, indent=2))

    # Create experiment record
    if "exp_id" in result:
        exp_json = workspace / "objects" / "experiment" / result["exp_id"] / f"{result['exp_id']}.json"
        exp_record = {
            "id": result["exp_id"],
            "type": "experiment",
            "state": result["status"],
            "attributes": {
                "method_id": args.method,
                "data_id": args.data,
                "config": config,
                "outputs": result.get("outputs", []),
                "lessons": result.get("lessons", "")
            }
        }
        with open(exp_json, 'w') as f:
            json.dump(exp_record, f, indent=2)

        state = load_state(workspace)
        is_new = result["exp_id"] not in state["objects"]
        state["objects"][result["exp_id"]] = {
            "type": "experiment",
            "state": result["status"],
            "path": str(exp_json.relative_to(workspace)),
        }
        if is_new:
            state["counts"]["experiment"] = state["counts"].get("experiment", 0) + 1
        save_state(workspace, state)

        append_event(
            workspace,
            {
                "action": "transition" if result["status"] == "completed" else "fail",
                "object_id": result["exp_id"],
                "object_type": "experiment",
                "state_after": result["status"],
                "reason": "Analysis execution completed"
                if result["status"] == "completed"
                else "Analysis execution failed",
                "details": {
                    "method_id": args.method,
                    "data_id": args.data,
                    "outputs": result.get("outputs", []),
                    "lessons": result.get("lessons", ""),
                },
            },
        )

if __name__ == "__main__":
    main()
