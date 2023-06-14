import pytest

from juniorguru.jobs.legacy_jobs.pipelines.junior_rank import WEIGHTS, calc_junior_rank


def test_calc_junior_rank_ignores_non_effective_features():
    assert calc_junior_rank([
        'ENGLISH_REQUIRED',
        'ENGLISH_REQUIRED',
        'ENGLISH_REQUIRED',
        'JUNIOR_FRIENDLY',
        'JUNIOR_FRIENDLY',
        'JUNIOR_FRIENDLY',
    ]) == 3 * WEIGHTS['JUNIOR_FRIENDLY']


def test_calc_junior_rank_accumulates_some_features():
    assert calc_junior_rank([
        'ENGLISH_REQUIRED',
        'JUNIOR_FRIENDLY',
        'JUNIOR_FRIENDLY',
        'JUNIOR_FRIENDLY',
    ]) == 3 * WEIGHTS['JUNIOR_FRIENDLY']


def test_calc_junior_rank_doesnt_accumulate_some_features():
    assert calc_junior_rank([
        'ENGLISH_REQUIRED',
        'TECH_DEGREE_REQUIRED',
        'TECH_DEGREE_REQUIRED',
        'JUNIOR_FRIENDLY',
        'JUNIOR_FRIENDLY',
    ]) == 1 * WEIGHTS['TECH_DEGREE_REQUIRED'] + 2 * WEIGHTS['JUNIOR_FRIENDLY']


def test_calc_junior_rank_penalizes_few_features_positive():
    few_features = ['JUNIOR_FRIENDLY', 'JUNIOR_FRIENDLY']
    few_features_rank = calc_junior_rank(few_features)

    enough_features = ['JUNIOR_FRIENDLY', 'JUNIOR_FRIENDLY', 'JUNIOR_FRIENDLY']
    enough_features_rank = calc_junior_rank(enough_features)

    assert few_features_rank == 2
    assert enough_features_rank == 3 * WEIGHTS['JUNIOR_FRIENDLY']


def test_calc_junior_rank_penalizes_few_features_zero():
    few_features = ['YEARS_EXPERIENCE_REQUIRED', 'JUNIOR_FRIENDLY']
    few_features_rank = calc_junior_rank(few_features)

    enough_features = ['YEARS_EXPERIENCE_REQUIRED', 'YEARS_EXPERIENCE_REQUIRED',
                       'JUNIOR_FRIENDLY']
    enough_features_rank = calc_junior_rank(enough_features)

    assert few_features_rank == 0
    assert enough_features_rank == (2 * WEIGHTS['YEARS_EXPERIENCE_REQUIRED'] +
                                    WEIGHTS['JUNIOR_FRIENDLY'])


def test_calc_junior_rank_penalizes_few_features_negative():
    few_features = ['YEARS_EXPERIENCE_REQUIRED', 'YEARS_EXPERIENCE_REQUIRED']
    few_features_rank = calc_junior_rank(few_features)

    enough_features = ['YEARS_EXPERIENCE_REQUIRED', 'YEARS_EXPERIENCE_REQUIRED',
                       'YEARS_EXPERIENCE_REQUIRED']
    enough_features_rank = calc_junior_rank(enough_features)

    assert few_features_rank == -2
    assert enough_features_rank == 3 * WEIGHTS['YEARS_EXPERIENCE_REQUIRED']


@pytest.mark.parametrize('features', [[f] for f in WEIGHTS.keys()])
def test_calc_junior_rank_one_feature_means_zero(features):
    assert calc_junior_rank(features) == 0
