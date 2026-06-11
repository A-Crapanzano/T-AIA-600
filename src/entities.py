from collections import Counter

import spacy

from src.fetch import cached, get_book_text

_NLP = None


def _nlp():
    global _NLP
    if _NLP is None:
        _NLP = spacy.load(
            "en_core_web_md",
            disable=["tagger", "parser", "lemmatizer", "attribute_ruler"],
        )
    return _NLP


def _chunks(text, size=100_000):
    start = 0
    while start < len(text):
        end = start + size
        if end < len(text):
            space = text.rfind(" ", start, end)
            if space > start:
                end = space
        yield text[start:end]
        start = end


@cached
def entities(book_id, min_occurrences=2):
    characters, locations = Counter(), Counter()
    for doc in _nlp().pipe(_chunks(get_book_text(book_id))):
        for ent in doc.ents:
            name = " ".join(ent.text.split()).replace("’", "'")
            name = name.removesuffix("'s").removesuffix("'")
            if not name or "CHAPTER" in name.upper():
                continue
            if ent.label_ == "PERSON":
                characters[name] += 1
            elif ent.label_ in ("GPE", "LOC"):
                locations[name] += 1

    for name in set(characters) & set(locations):
        if characters[name] >= locations[name]:
            del locations[name]
        else:
            del characters[name]

    return {
        "characters": sorted(n for n, c in characters.items() if c >= min_occurrences),
        "locations": sorted(n for n, c in locations.items() if c >= min_occurrences),
    }
