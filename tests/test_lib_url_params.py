import pytest

from jg.coop.lib.url_params import get_params, strip_params


def test_get_params():
    url = "https://4value-group.jobs.cz/detail-pozice?r=detail&id=2000142365&rps=228&impressionId=a653a2a6-05c9-49fb-b391-96b185355f2d"

    assert get_params(url) == dict(
        r="detail",
        id="2000142365",
        rps="228",
        impressionId="a653a2a6-05c9-49fb-b391-96b185355f2d",
    )


@pytest.mark.parametrize(
    "url,param_names,expected",
    [
        ("https://example.com", ["a", "b"], "https://example.com"),
        ("https://example.com?a=1&b=2", ["a", "b"], "https://example.com"),
        ("https://example.com?a=1&c=3&b=2", ["a", "b"], "https://example.com?c=3"),
        ("https://example.com", [], "https://example.com"),
        ("https://example.com?a=1&b=2", [], "https://example.com?a=1&b=2"),
    ],
)
def test_strip_params(url, param_names, expected):
    assert strip_params(url, param_names) == expected
