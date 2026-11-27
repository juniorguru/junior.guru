from jg.coop.web.context import build_love_context


def test_build_love_context_donations_coverage():
    context = build_love_context(
        {"donations": 2100, "memberships": 6000}, 10000, github_sponsors_czk=89
    )

    assert context["donations_coverage_ptc"] == 21


def test_build_love_context_no_cost():
    context = build_love_context({"donations": 2100}, 0, github_sponsors_czk=89)

    assert context["donations_coverage_ptc"] is None


def test_build_love_context_github_sponsors_czk():
    context = build_love_context({}, 10000, github_sponsors_czk=89)

    assert context["github_sponsors_czk"] == 89


def test_build_love_context_donation_amount():
    context = build_love_context({}, 10000, github_sponsors_czk=89)

    assert context["donation_amount_czk"] == 499


def test_build_love_context_qr_svg():
    context = build_love_context({}, 10000, github_sponsors_czk=89)

    assert str(context["donation_qr_svg"]).startswith("<svg ")
