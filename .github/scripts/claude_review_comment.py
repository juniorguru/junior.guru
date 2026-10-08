"""Posts a PR comment with the outcome of the Claude review, whatever happened"""

import json
import os
import subprocess
from pathlib import Path


TITLES = {"issues": "found issues", "ok": "no issues found", "skipped": "skipped"}


def get_failure_reason(step_outcome: str) -> str:
    execution_file = Path(os.environ["RUNNER_TEMP"]) / "claude-execution-output.json"
    try:
        messages = json.loads(execution_file.read_text())
        result = [message for message in messages if message["type"] == "result"][-1]
        reason = (
            result.get("result")
            or "\n".join(result.get("errors", []))
            or result["subtype"]
        )
    except (FileNotFoundError, IndexError, KeyError, json.JSONDecodeError):
        reason = "Claude produced no result, see the logs."
    return f"Step outcome: `{step_outcome}`\n\n{reason}"


def main() -> None:
    step_outcome = os.environ["CLAUDE_OUTCOME"]
    structured_output = os.environ["STRUCTURED_OUTPUT"]

    if step_outcome == "success" and structured_output:
        review = json.loads(structured_output)
        title = TITLES.get(review["outcome"], review["outcome"])
        summary = review["summary"]
    elif step_outcome == "success":
        title = "skipped"
        summary = (
            "The Claude action exited without running Claude. It does that e.g. on PRs "
            "changing this workflow file, which must match the default branch. "
            "See the warning in the logs."
        )
    else:
        title = "failed"
        summary = get_failure_reason(step_outcome)

    body = (
        f"## Claude review: {title}\n\n{summary}\n\n[Logs]({os.environ['RUN_URL']})\n"
    )
    subprocess.run(
        ["gh", "pr", "comment", os.environ["PR_NUMBER"], "--body", body], check=True
    )


if __name__ == "__main__":
    main()
