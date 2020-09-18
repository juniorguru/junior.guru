import pytest

from juniorguru.scrapers.pipelines.jg_rank_filter import Pipeline, NotEntryLevel


@pytest.mark.parametrize('rank', [1, 20, 420])
def test_jg_rank_filter(item, spider, rank):
    item['jg_rank'] = rank
    item = Pipeline().process_item(item, spider)

    assert item['jg_rank'] == rank


@pytest.mark.parametrize('rank', [-420, -20, -1, 0])
def test_jg_rank_filter_drops(item, spider, rank):
    item['jg_rank'] = rank

    with pytest.raises(NotEntryLevel, match=str(rank)):
        Pipeline().process_item(item, spider)
