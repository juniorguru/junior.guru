import re


COUPON_RE = re.compile(r'''
    ^
        (?P<name>
            (?P<student_prefix>STUDENT)?
            [A-Z0-9]+
            [A-Z]+
        )
        (?P<suffix>[0-9]{5,})
    $
''', re.VERBOSE)


def parse_coupon(coupon):
    match = COUPON_RE.match(coupon)
    if match:
        parts = match.groupdict()
        parts['coupon'] = ''.join([
            parts['name'],
            parts['suffix'],
        ])
        parts['is_student'] = bool(parts.pop('student_prefix'))
        return {key: value for key, value in parts.items() if value is not None}
    return {'name': coupon, 'coupon': coupon, 'is_student': False}
