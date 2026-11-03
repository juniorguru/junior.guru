from datetime import UTC, datetime

import pytest

from jg.coop.cli.cancel_previous_builds import (
    get_recent_runs,
    get_run_branch,
    get_run_number,
    get_workflows_to_cancel,
)


def create_workflow(id: str, phase: str, created_at: str) -> dict:
    return {
        "id": id,
        "attributes": {"phase": phase, "created_at": created_at},
        "references": {"run": {"id": f"run-{id}"}},
    }


def test_get_workflows_to_cancel():
    workflows = [
        create_workflow("older", "started", "2026-11-03T10:00:00.000Z"),
        create_workflow("older-ended", "ended", "2026-11-03T10:00:00.000Z"),
        create_workflow("current", "started", "2026-11-03T11:00:00.000Z"),
        create_workflow("newer", "started", "2026-11-03T12:00:00.000Z"),
    ]

    assert [w["id"] for w in get_workflows_to_cancel(workflows, "current")] == ["older"]


@pytest.mark.parametrize(
    "event_attributes, expected",
    [
        ({"type": "push", "vcs": {"branch": "main"}}, "main"),
        ({"type": "unknown"}, None),
    ],
)
def test_get_run_branch(event_attributes: dict, expected: str | None):
    run = {"references": {"event": {"attributes": event_attributes}}}

    assert get_run_branch(run) == expected


def test_get_run_number():
    workflow = create_workflow("abc", "started", "2026-11-03T10:00:00.000Z")
    runs = [
        {"id": "run-xyz", "attributes": {"number": 41}},
        {"id": "run-abc", "attributes": {"number": 42}},
    ]

    assert get_run_number(workflow, runs) == 42


def test_get_recent_runs():
    runs = iter(
        [
            {"id": "new", "attributes": {"created_at": "2026-11-03T10:00:00.000Z"}},
            {"id": "old", "attributes": {"created_at": "2026-10-30T10:00:00.000Z"}},
            {"id": "new2", "attributes": {"created_at": "2026-11-03T09:00:00.000Z"}},
        ]
    )
    since = datetime(2026, 11, 1, tzinfo=UTC)

    assert [run["id"] for run in get_recent_runs(runs, since)] == ["new"]
