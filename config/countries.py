COUNTRY_LIST = [
    ("PL", "Polska"),
    ("SK", "Slowacja"),
    ("CZ", "Czechy"),
    ("DE", "Niemcy"),
    ("AT", "Austria"),
    ("HU", "Wegry"),
    ("LT", "Litwa"),
    ("LV", "Lotwa"),
    ("EE", "Estonia"),
    ("UA", "Ukraina"),
    ("RO", "Rumunia"),
    ("BG", "Bulgaria"),
    ("HR", "Chorwacja"),
    ("SI", "Slowenia"),
    ("SE", "Szwecja"),
]

COUNTRY_CHOICES = tuple(COUNTRY_LIST)
COUNTRY_LOOKUP = {code: name for code, name in COUNTRY_LIST}
DEFAULT_COUNTRY_CODE = COUNTRY_CHOICES[0][0] if COUNTRY_CHOICES else ""


def country_choices():
    return COUNTRY_CHOICES


def country_name_for(code: str) -> str:
    if not code:
        return ""
    return COUNTRY_LOOKUP.get(code.upper(), "")
