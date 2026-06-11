import re

_TOKEN_RE = re.compile(r"[^\W\d_]+")


def tokenize(text):
    return _TOKEN_RE.findall(text.casefold())
