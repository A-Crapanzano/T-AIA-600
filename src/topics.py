import math
import re
from collections import Counter

from src.text import tokenize

_TOP_K = 10

_CHAPTER_RE = re.compile(
    r"^\s*(?:(?:CHAPTER|Chapter|CHAP\.|PART|BOOK)\s+[\dIVXLCDM]+"
    r"|[\dIVXLCDM]+\.\s+[A-Z][A-Z ]{3,})",
    re.MULTILINE,
)

_MIN_CHAPTERS = 3
_MIN_SECTION_TOKENS = 50
_TARGET_SECTION_TOKENS = 1500
_MIN_FALLBACK = 4


def _split_by_chapters(text):
    starts = [m.start() for m in _CHAPTER_RE.finditer(text)]
    if len(starts) < _MIN_CHAPTERS:
        return None
    bounds = [*starts, len(text)]
    sections = [
        tokens
        for i in range(len(starts))
        if len(tokens := tokenize(text[bounds[i] : bounds[i + 1]]))
        >= _MIN_SECTION_TOKENS
    ]
    return sections if len(sections) >= _MIN_CHAPTERS else None


def _split_equal(text):
    tokens = tokenize(text)
    if not tokens:
        return []
    n = max(_MIN_FALLBACK, round(len(tokens) / _TARGET_SECTION_TOKENS))
    n = min(n, len(tokens))
    base, extra = divmod(len(tokens), n)
    sections, start = [], 0
    for i in range(n):
        size = base + (1 if i < extra else 0)
        sections.append(tokens[start : start + size])
        start += size
    return sections


def split_sections(text):
    return _split_by_chapters(text) or _split_equal(text)


def _top_keywords(sections, k=_TOP_K):
    counts = [Counter(section) for section in sections]
    n = len(counts)
    df = Counter()
    for count in counts:
        df.update(count.keys())

    result = {}
    for i, count in enumerate(counts, start=1):
        length = count.total()
        scores = {
            word: (freq / length) * math.log(n / df[word])
            for word, freq in count.items()
        }
        result[i] = sorted(scores, key=scores.get, reverse=True)[:k]
    return result


def topics(text):
    return _top_keywords(split_sections(text))
