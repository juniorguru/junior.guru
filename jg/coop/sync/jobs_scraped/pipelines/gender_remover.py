import re


GENDER_RES = [
    # in parentheses, e.g. (f/m/*)
    re.compile(
        r"""
            \s*                     # trailing spaces
            \(                      # opening parenthesis
                \s*[mfwžhd]\s*      # woman/man letter (with spaces)
                [/\|]               # slash or pipe
                \s*[mfwžhd]\s*      # woman/man letter (with spaces)
                (                   # optionally:
                    [/\|]           # slash or pipe
                    \s*[^\)]+\s*    # anything but closing bracket (with spaces)
                )?
            \)                      # closing parenthesis
            \s*                     # trailing spaces
        """,
        re.VERBOSE | re.IGNORECASE,
    ),
    # no parentheses, e.g. f/m/x
    re.compile(
        r"""
            (\-\s*)?        # optional leading dash
            [mfwžhd]\s*     # woman/man letter (with spaces)
            [/\|]           # slash or pipe
            \s*[mfwžhd]\s*  # woman/man letter (with spaces)
            (               # optionally:
                [/\|]       # slash or pipe
                \s*\w+      # anything but space or end
            )?
        """,
        re.VERBOSE | re.IGNORECASE,
    ),
    # emojis
    re.compile(r"👩‍💻[\/\|]👨‍💻|👨‍💻[\/\|]👩‍💻"),
    # 'all genders'
    re.compile(r"\(\s*all\s+genders\s*\)"),
    re.compile(r"\(\s*all\s+humans\s*\)"),
]


async def process(item: dict) -> dict:
    for gender_re in GENDER_RES:
        item["title"] = gender_re.sub(" ", item["title"]).strip()
    return item
