import re


COUPON_RE = re.compile(r'''
    ^
        (?P<slug>
            (?P<student_prefix>STUDENT)?
            [A-Z0-9]+
            [A-Z]+
        )
        (?P<suffix>[0-9]{5,})
    $
''', re.VERBOSE)


def parse_coupon(coupon):
    if match := COUPON_RE.match(coupon):
        parts = match.groupdict()
        parts['coupon'] = ''.join([
            parts['slug'],
            parts['suffix'],
        ])
        parts['slug'] = parts['slug'].lower()
        parts['is_student'] = bool(parts.pop('student_prefix'))
        return {key: value for key, value in parts.items() if value is not None}
    return {'slug': coupon.lower(), 'coupon': coupon, 'is_student': False}
