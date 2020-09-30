import re


def rule(pattern, value, ignorecase=True):
    compile_flags = re.IGNORECASE if ignorecase else 0
    return (re.compile(r'\b' + pattern + r'\b', compile_flags), value)


COUNTRIES = dict([
    rule(r'CZ', 'Česko', ignorecase=False),
    rule(r'ČR', 'Česko', ignorecase=False),
    rule(r'Česko', 'Česko'),
    rule(r'Czechia', 'Česko'),
    rule(r'Česk\w+ Rep(\.|\w+)', 'Česko'),
    rule(r'(The )?Czech Rep(\.|\w+)', 'Česko'),
    rule(r'SK', 'Slovensko', ignorecase=False),
    rule(r'SR', 'Slovensko', ignorecase=False),
    rule(r'Slovensko', 'Slovensko'),
    rule(r'Slovakia', 'Slovensko'),
    rule(r'Slovak\w* Rep(\.|\w+)', 'Slovensko'),
    rule(r'(The )?Slovak Rep(\.|\w+)', 'Slovensko'),
])
REGIONS = dict([
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
    default_country = 'Česko'

    def process_item(self, item, spider):
        country, region = parse_location(item['location'])
        item['location_country'] = (
            country or
            getattr(spider, 'default_country', None) or
            self.default_country
        )
        item['location_region'] = region
        return item


def parse_location(location):
    parts = [part.strip() for part in location.split(',')]

    country = None
    region = None

    while parts:
        part = parts.pop()
        part_is_country = False
        if not country:
            for country_re, c in COUNTRIES.items():
                if country_re.search(part):
                    country = c
                    part_is_country = True
                    break
        if not part_is_country and not region:
            for region_re, r in REGIONS.items():
                if region_re.search(part):
                    region = r
                    break
        if country and region:
            break

    return country, region


# def match_areas(parts, areas):
#     for area_re, area in areas.items():
#         for part in parts:
#             if area_re.search(part):
#                 return area, area_re
#     return None, None
