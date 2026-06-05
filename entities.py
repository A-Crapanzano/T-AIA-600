from collections import Counter
from tools import get_nlp, download_book, clean_gutenberg_text


def entities(book_id, min_occurrences=2):
    path = download_book(book_id)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = clean_gutenberg_text(text)

    nlp = get_nlp()
    doc = nlp(text)

    char_counts = Counter()
    loc_counts = Counter()

    for ent in doc.ents:
        name = ent.text.strip()

        if not name or "\n" in name or "CHAPTER" in name.upper():
            continue

        name = name.replace("\u2019", "'")

        if ent.label_ == "PERSON":
            char_counts[name] += 1
        elif ent.label_ in ("GPE", "LOC"):
            loc_counts[name] += 1

    characters = sorted(
        name for name, count in char_counts.items() if count >= min_occurrences
    )
    locations = sorted(
        name for name, count in loc_counts.items() if count >= min_occurrences
    )

    return {
        "characters": characters,
        "locations": locations,
    }