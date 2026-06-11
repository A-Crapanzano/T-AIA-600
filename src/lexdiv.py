from collections import Counter

from src.text import tokenize


def lexdiv(text):
    tokens = tokenize(text)
    counts = Counter(tokens)
    tok = len(tokens)
    typ = len(counts)
    hap = sum(1 for c in counts.values() if c == 1)

    return {
        "tok": tok,
        "typ": typ,
        "hap": hap,
        "ttr": typ / tok if tok else 0.0,
        "mwl": sum(len(t) for t in tokens) / tok if tok else 0.0,
        "mwf": tok / typ if typ else 0.0,
    }


def _mattr(tokens, window=100):
    n = len(tokens)
    if n <= window:
        return len(set(tokens)) / n if n else 0.0

    counts = Counter(tokens[:window])
    total = len(counts) / window
    n_windows = n - window + 1
    for i in range(1, n_windows):
        out = tokens[i - 1]
        counts[out] -= 1
        if counts[out] == 0:
            del counts[out]
        counts[tokens[i + window - 1]] += 1
        total += len(counts) / window
    return total / n_windows


def _mtld_pass(tokens, threshold=0.72):
    factors = 0.0
    types = set()
    count = 0
    for tok in tokens:
        types.add(tok)
        count += 1
        if len(types) / count <= threshold:
            factors += 1
            types, count = set(), 0
    if count:
        factors += (1 - len(types) / count) / (1 - threshold)
    return len(tokens) / factors if factors else 0.0


def _mtld(tokens, threshold=0.72):
    if not tokens:
        return 0.0
    return (_mtld_pass(tokens, threshold) + _mtld_pass(tokens[::-1], threshold)) / 2


def advanced_diversity(text):
    tokens = tokenize(text)
    return {"mattr": _mattr(tokens), "mtld": _mtld(tokens)}
