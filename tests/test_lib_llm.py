import pytest
from openai.types.responses import Response

from jg.coop.lib.llm import describe_response


def create_response(**kwargs) -> Response:
    values = {
        "id": "resp",
        "created_at": 0,
        "model": "gpt-4.1",
        "object": "response",
        "output": [],
        "parallel_tool_calls": False,
        "tool_choice": "auto",
        "tools": [],
        "status": "completed",
    }
    values.update(kwargs)
    return Response.model_validate(values)


def message(*content: dict) -> dict:
    return {
        "type": "message",
        "id": "msg",
        "role": "assistant",
        "status": "completed",
        "content": list(content),
    }


def test_describe_response_empty():
    response = create_response()

    assert describe_response(response) == "status='completed', output_text='' (0 chars)"


def test_describe_response_incomplete():
    response = create_response(
        status="incomplete",
        incomplete_details={"reason": "max_output_tokens"},
    )

    assert "incomplete_reason='max_output_tokens'" in describe_response(response)


def test_describe_response_error():
    response = create_response(error={"code": "server_error", "message": "Boom"})

    assert "error='server_error': 'Boom'" in describe_response(response)


def test_describe_response_refusal():
    response = create_response(
        output=[message({"type": "refusal", "refusal": "No."})],
    )

    assert "refusal='No.'" in describe_response(response)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", "output_text='' (0 chars)"),
        ('{"topics": []}', "output_text='{\"topics\": []}' (14 chars)"),
    ],
)
def test_describe_response_output_text(text, expected):
    response = create_response(
        output=[message({"type": "output_text", "text": text, "annotations": []})],
    )

    assert expected in describe_response(response)
