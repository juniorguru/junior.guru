import pytest

from jg.coop.models.candidate import Candidate
from jg.coop.models.club import ClubUser

from testing_utils import prepare_test_db


@pytest.fixture
def test_db():
    yield from prepare_test_db([ClubUser, Candidate])


def create_candidate(**kwargs):
    return Candidate.create(
        github_username=kwargs.get("github_username", "alice"),
        github_url=kwargs.get("github_url", "https://github.com/alice"),
        name=kwargs.get("name", "Alice"),
        avatar_url=kwargs.get("avatar_url", "https://avatars.example.com/alice.png"),
        avatar_is_default=kwargs.get("avatar_is_default", False),
        is_ready=kwargs.get("is_ready", True),
        is_member=kwargs.get("is_member", False),
        secondary_school=kwargs.get("secondary_school"),
        university=kwargs.get("university"),
    )


@pytest.mark.parametrize(
    "secondary_school, university, expected",
    (
        (None, None, ""),
        ("it", None, "IT střední"),
        ("math", None, "matematická střední"),
        ("non_it", None, "střední"),
        (None, "it", "IT vysoká"),
        (None, "math", "matematická vysoká"),
        ("it", "math", "IT střední, matematická vysoká"),
        ("non_it", "it", "IT vysoká"),
    ),
)
def test_school_text(test_db, secondary_school, university, expected):
    candidate = create_candidate(
        secondary_school=secondary_school, university=university
    )

    assert candidate.school_text == expected


@pytest.mark.parametrize(
    "secondary_school,university",
    (
        ("unexpected", None),
        (None, "unexpected"),
    ),
)
def test_school_text_raises_key_error_for_unknown_prefix(
    test_db, secondary_school, university
):
    candidate = create_candidate(
        secondary_school=secondary_school, university=university
    )

    with pytest.raises(KeyError):
        _ = candidate.school_text
