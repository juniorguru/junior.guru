import pytest
from pydantic import BaseModel, ValidationError

from jg.coop.lib.llm import is_empty_response_error


class DummySchema(BaseModel):
    number: int


def make_validation_error(json_text: str) -> ValidationError:
    try:
        DummySchema.model_validate_json(json_text)
    except ValidationError as error:
        return error
    raise AssertionError("Expected a ValidationError")


@pytest.mark.parametrize("json_text", ["", "   ", "\n\t"])
def test_is_empty_response_error_true(json_text):
    assert is_empty_response_error(make_validation_error(json_text)) is True


@pytest.mark.parametrize(
    "json_text",
    ['{"number":', '{"number": "not an int"}', '{"other": 1}'],
)
def test_is_empty_response_error_false(json_text):
    assert is_empty_response_error(make_validation_error(json_text)) is False
