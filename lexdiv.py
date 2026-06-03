from collections import Counter
from tools import get_book_tokens


def lexdiv(book_id):
    """Calcule les métriques de diversité lexicale d'un livre."""
    words = get_book_tokens(book_id)
    counts = Counter(words)

    tok = len(words)
    typ = len(set(words))
    hap = sum(1 for count in counts.values() if count == 1)
    ttr = typ / tok
    mwl = sum(len(word) for word in words) / tok
    mwf = tok / typ

    return {
        "tok": tok,
        "typ": typ,
        "hap": hap,
        "ttr": ttr,
        "mwl": mwl,
        "mwf": mwf,
    }