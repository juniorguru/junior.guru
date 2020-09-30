import re

import geocoder


def rule(pattern, value, ignorecase=True):
    compile_flags = re.IGNORECASE if ignorecase else 0
    return (re.compile(r'\b' + pattern + r'\b', compile_flags), value)


REGIONS = dict([
    # https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_na_Slovensku
    rule(r'SK', 'Slovensko', ignorecase=False),
    rule(r'SR', 'Slovensko', ignorecase=False),
    rule(r'Slovensko', 'Slovensko'),
    rule(r'Slovakia', 'Slovensko'),
    rule(r'Slovak\w* Rep(\.|\w+)', 'Slovensko'),
    rule(r'(The )?Slovak Rep(\.|\w+)', 'Slovensko'),
    rule(r'Bratislava', 'Slovensko'),
    rule(r'Košice', 'Slovensko'),
    rule(r'Prešov', 'Slovensko'),
    rule(r'Žilina', 'Slovensko'),
    rule(r'Nitra', 'Slovensko'),
    rule(r'Banská Bystrica', 'Slovensko'),
    rule(r'B(\.|\w+) Bystrica', 'Slovensko'),
    rule(r'Banská B(\.|\w+)', 'Slovensko'),
    rule(r'Trnava', 'Slovensko'),
    rule(r'Martin', 'Slovensko'),
    rule(r'Trenčín', 'Slovensko'),
    rule(r'Poprad', 'Slovensko'),
    rule(r'Prievidza', 'Slovensko'),

    # https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Poland
    rule(r'PL', 'Polsko', ignorecase=False),
    rule(r'Polsko', 'Polsko'),
    rule(r'Poland', 'Polsko'),
    rule(r'Polska', 'Polsko'),
    rule(r'Warsaw', 'Polsko'),
    rule(r'Varšava', 'Polsko'),
    rule(r'Warszawa', 'Polsko'),
    rule(r'Krak[óo]w', 'Polsko'),
    rule(r'Cracow', 'Polsko'),
    rule(r'Krakov', 'Polsko'),
    rule(r'Wroc[łl]aw', 'Polsko'),
    rule(r'Vratislav', 'Polsko'),
    rule(r'Kato[wv]ic[ey]', 'Polsko'),

    # https://en.wikipedia.org/wiki/List_of_cities_in_Germany_by_population
    rule(r'DE', 'Německo', ignorecase=False),
    rule(r'Německo', 'Německo'),
    rule(r'Germany', 'Německo'),
    rule(r'Deutsch(\.|\w+)', 'Německo'),
    rule(r'Berl[ií]n', 'Německo'),
    rule(r'Leipzig', 'Německo'),
    rule(r'Lipsko', 'Německo'),
    rule(r'Dresden', 'Německo'),
    rule(r'Drážďany', 'Německo'),
    rule(r'N[uü]rnberg', 'Německo'),
    rule(r'Nuremberg', 'Německo'),
    rule(r'Norimberk', 'Německo'),
    rule(r'M[uü]nchen', 'Německo'),
    rule(r'Munich', 'Německo'),
    rule(r'Mnichov', 'Německo'),

    # https://en.wikipedia.org/wiki/List_of_cities_and_towns_in_Austria
    rule(r'AT', 'Rakousko', ignorecase=False),
    rule(r'Rakousko', 'Rakousko'),
    rule(r'Austria', 'Rakousko'),
    rule(r'[ÖO]sterreich', 'Rakousko'),
    rule(r'Vienna', 'Rakousko'),
    rule(r'Vídeň', 'Rakousko'),
    rule(r'Wien', 'Rakousko'),
    rule(r'Linz', 'Rakousko'),
    rule(r'Linec', 'Rakousko'),

    # https://cs.wikipedia.org/wiki/Kraje_v_%C4%8Cesku
    # https://en.wikipedia.org/wiki/Regions_of_the_Czech_Republic
    rule(r'(Hlavní město )?Pra(ha|gue)', 'Praha'),
    rule(r'Středočeský( kraj)?', 'Praha'),
    rule(r'Central Bohemian', 'Praha'),
    rule(r'Jihočeský ( kraj)?', 'České Budějovice'),
    rule(r'South Bohemian', 'České Budějovice'),
    rule(r'Č(\.|\w+) Budějovice', 'České Budějovice'),
    rule(r'(Kraj )?Vysočina', 'Jihlava'),
    rule(r'Jihlava', 'Jihlava'),
    rule(r'Plzeňský( kraj)?', 'Plzeň'),
    rule(r'Plzeň', 'Plzeň'),
    rule(r'Pilsen', 'Plzeň'),
    rule(r'Karlovarský( kraj)?', 'Karlovy Vary'),
    rule(r'K(\.|\w+) Vary', 'Karlovy Vary'),
    rule(r'Ústecký( kraj)?', 'Ústí nad Labem'),
    rule(r'Ústí nad Labem', 'Ústí nad Labem'),
    rule(r'Ústí n\w*\. ?L\w*\.', 'Ústí nad Labem'),
    rule(r'Ústí n\.?/?L\.?', 'Ústí nad Labem'),
    rule(r'Liberecký( kraj)?', 'Liberec'),
    rule(r'Liberec', 'Liberec'),
    rule(r'Královéhradecký( kraj)?', 'Hradec Králové'),
    rule(r'Hradec Králové', 'Hradec Králové'),
    rule(r'H(\.|\w+) Králové', 'Hradec Králové'),
    rule(r'Hradec K(\.|\w+)', 'Hradec Králové'),
    rule(r'Pardubický( kraj)?', 'Pardubice'),
    rule(r'Pardubice', 'Pardubice'),
    rule(r'Olomoucký( kraj)?', 'Olomouc'),
    rule(r'Olomouc', 'Olomouc'),
    rule(r'Moravskoslezský( kraj)?', 'Ostrava'),
    rule(r'Moravian-Silesian', 'Ostrava'),
    rule(r'Ostrava', 'Ostrava'),
    rule(r'Jihomoravský( kraj)?', 'Brno'),
    rule(r'South Moravian', 'Brno'),
    rule(r'Brno', 'Brno'),
    rule(r'Zlínský( kraj)?', 'Zlín'),
    rule(r'Zlín', 'Zlín'),

    # https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku_podle_po%C4%8Dtu_obyvatel
    rule(r'Havířov', 'Ostrava'),
    rule(r'Kladno', 'Praha'),
    rule(r'Most', 'Ústí nad Labem'),
    rule(r'Opava', 'Ostrava'),
    rule(r'Frýdek-Místek', 'Ostrava'),
    rule(r'Karviná', 'Ostrava'),
    rule(r'Teplice', 'Ústí nad Labem'),
    rule(r'Chomutov', 'Ústí nad Labem'),
    rule(r'Děčín', 'Ústí nad Labem'),
    rule(r'Jablonec nad Nisou', 'Liberec'),
])


class Pipeline():
    def __init__(self, stats=None, geocode=None):
        self.stats = stats
        self.geocode = geocode

    @classmethod
    def from_crawler(cls, crawler):
        return cls(stats=crawler.stats, geocode=geocode)

    def process_item(self, item, spider):
        region = detect_region(item['location'])
        if not region and self.geocode:
            region = self.geocode(item['location'])
            if self.stats:
                self.stats.inc_value('item_geocoded_count')
        item['region'] = region
        return item


def detect_region(location):
    for part in [part.strip() for part in location.split(',')]:
        for region_re, region in REGIONS.items():
            if region_re.search(part):
                return region


def geocode(location):
    response = geocoder.osm(location).json
    return response


# if __name__ == "__main__":
#     from pprint import pprint
#     pprint(geocode('Káranice, Hradec Králové, Czech Republic'))
#     # geocode('252 30 Řevnice, Česko')
