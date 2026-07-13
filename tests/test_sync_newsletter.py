import pytest

from jg.coop.lib.buttondown import ButtondownError
from jg.coop.sync.newsletter import delete_old_drafts, select_drafts_to_delete


def draft(draft_id: str, creation_date: str, status: str = "draft") -> dict:
    return {
        "id": draft_id,
        "creation_date": creation_date,
        "status": status,
        "subject": f"Draft {draft_id}",
    }


class FakeButtondownAPI:
    def __init__(self, emails: list[dict]):
        self._emails = emails
        self.deleted_ids: list[str] = []

    async def get_drafts(self):
        for email in self._emails:
            yield email

    async def delete_email(self, email_id: str) -> None:
        self.deleted_ids.append(email_id)


@pytest.mark.parametrize(
    "emails, max_drafts, expected_ids",
    [
        pytest.param(
            [
                draft("a", "2026-01-01T00:00:00Z"),
                draft("b", "2026-04-01T00:00:00Z"),
                draft("c", "2026-03-01T00:00:00Z"),
                draft("d", "2026-02-01T00:00:00Z"),
            ],
            3,
            ["a"],
            id="deletes-oldest-beyond-limit",
        ),
        pytest.param(
            [
                draft("a", "2026-01-01T00:00:00Z"),
                draft("b", "2026-02-01T00:00:00Z"),
            ],
            3,
            [],
            id="keeps-all-within-limit",
        ),
        pytest.param(
            [
                draft("a", "2026-01-01T00:00:00Z"),
                draft("sent", "2026-05-01T00:00:00Z", status="sent"),
                draft("b", "2026-04-01T00:00:00Z"),
                draft("c", "2026-03-01T00:00:00Z"),
                draft("d", "2026-02-01T00:00:00Z"),
            ],
            3,
            ["a"],
            id="never-selects-non-drafts",
        ),
        pytest.param(
            [
                draft("a", "2026-01-01T00:00:00Z"),
                draft("b", "2026-02-01T00:00:00Z"),
            ],
            0,
            ["b", "a"],
            id="zero-limit-selects-all-drafts",
        ),
        pytest.param([], 3, [], id="empty-input"),
    ],
)
def test_select_drafts_to_delete(emails, max_drafts, expected_ids):
    selected = select_drafts_to_delete(emails, max_drafts)

    assert [email["id"] for email in selected] == expected_ids


@pytest.mark.asyncio
async def test_delete_old_drafts_deletes_selected():
    api = FakeButtondownAPI(
        [
            draft("a", "2026-01-01T00:00:00Z"),
            draft("b", "2026-03-01T00:00:00Z"),
            draft("c", "2026-02-01T00:00:00Z"),
        ]
    )

    await delete_old_drafts(api, max_drafts=2)

    assert api.deleted_ids == ["a"]


@pytest.mark.asyncio
async def test_delete_old_drafts_continues_after_failure():
    class FlakyAPI(FakeButtondownAPI):
        async def delete_email(self, email_id: str) -> None:
            if email_id == "a":
                raise ButtondownError("boom")
            await super().delete_email(email_id)

    api = FlakyAPI(
        [
            draft("a", "2026-01-01T00:00:00Z"),
            draft("b", "2026-02-01T00:00:00Z"),
            draft("c", "2026-03-01T00:00:00Z"),
        ]
    )

    await delete_old_drafts(api, max_drafts=1)

    assert api.deleted_ids == ["b"]
