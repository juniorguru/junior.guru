import pytest

from jg.coop.sync.newsletter import delete_old_drafts


class FakeButtondownAPI:
    def __init__(self, drafts: list[dict]):
        self._drafts = drafts
        self.deleted_ids: list[str] = []

    async def get_drafts(self):
        for draft in self._drafts:
            yield draft

    async def delete_email(self, email_id: str) -> None:
        self.deleted_ids.append(email_id)


def draft(id: str, creation_date: str, status: str = "draft") -> dict:
    return {
        "id": id,
        "creation_date": creation_date,
        "status": status,
        "subject": f"Draft {id}",
    }


@pytest.mark.asyncio
async def test_delete_old_drafts_keeps_most_recent():
    api = FakeButtondownAPI(
        [
            draft("a", "2026-01-01T00:00:00Z"),
            draft("b", "2026-04-01T00:00:00Z"),
            draft("c", "2026-03-01T00:00:00Z"),
            draft("d", "2026-02-01T00:00:00Z"),
        ]
    )

    await delete_old_drafts(api, max_drafts=3)

    assert api.deleted_ids == ["a"]


@pytest.mark.asyncio
async def test_delete_old_drafts_noop_below_limit():
    api = FakeButtondownAPI(
        [
            draft("a", "2026-01-01T00:00:00Z"),
            draft("b", "2026-02-01T00:00:00Z"),
        ]
    )

    await delete_old_drafts(api, max_drafts=3)

    assert api.deleted_ids == []


@pytest.mark.asyncio
async def test_delete_old_drafts_ignores_non_drafts():
    api = FakeButtondownAPI(
        [
            draft("a", "2026-01-01T00:00:00Z"),
            draft("sent", "2026-05-01T00:00:00Z", status="sent"),
            draft("b", "2026-04-01T00:00:00Z"),
            draft("c", "2026-03-01T00:00:00Z"),
            draft("d", "2026-02-01T00:00:00Z"),
        ]
    )

    await delete_old_drafts(api, max_drafts=3)

    assert "sent" not in api.deleted_ids
    assert api.deleted_ids == ["a"]
