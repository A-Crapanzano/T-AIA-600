from tools import get_nlp, download_book, clean_gutenberg_text


def entities(book_id):
    path = download_book(book_id)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = clean_gutenberg_text(text)

    nlp = get_nlp()
    doc = nlp(text)

    characters = set()
    locations = set()

    for ent in doc.ents:
        name = ent.text.strip()
        if not name:
            continue

        if ent.label_ == "PERSON":
            characters.add(name)
        elif ent.label_ == "GPE" or ent.label_ == "LOC":
            locations.add(name)

    return {
        "characters": sorted(characters),
        "locations": sorted(locations),
    }