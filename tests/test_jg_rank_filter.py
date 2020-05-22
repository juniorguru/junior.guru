from juniorguru.scrapers.pipelines.jg_rank_filter import (
    FEW_FEATURES_PENALTY, FEW_FEATURES_THRESHOLD, WEIGHTS, calc_jg_rank)


def test_calc_jg_rank_ignores_non_effective_features():
    assert calc_jg_rank([
        'ENGLISH_REQUIRED',
        'ENGLISH_REQUIRED',
        'ENGLISH_REQUIRED',
        'JUNIOR_FRIENDLY',
    ]) == WEIGHTS['JUNIOR_FRIENDLY']


def test_calc_jg_rank_accumulates_some_features():
    assert calc_jg_rank([
        'ENGLISH_REQUIRED',
        'JUNIOR_FRIENDLY',
        'JUNIOR_FRIENDLY',
    ]) == 2 * WEIGHTS['JUNIOR_FRIENDLY']


def test_calc_jg_rank_doesnt_accumulate_some_features():
    assert calc_jg_rank([
        'ENGLISH_REQUIRED',
        'TECH_DEGREE_REQUIRED',
        'TECH_DEGREE_REQUIRED',
    ]) == 1 * WEIGHTS['TECH_DEGREE_REQUIRED']


def test_calc_jg_rank_penalizes_few_features():
    few_features = FEW_FEATURES_THRESHOLD * ['JUNIOR_FRIENDLY']
    few_features_rank = calc_jg_rank(few_features)

    enough_features = (FEW_FEATURES_THRESHOLD + 1) * ['JUNIOR_FRIENDLY']
    enough_features_rank = calc_jg_rank(enough_features)

    assert few_features_rank < enough_features_rank
    assert few_features_rank < (enough_features_rank * FEW_FEATURES_PENALTY)
