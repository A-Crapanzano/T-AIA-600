import math
from collections import Counter

from src.collection import COLLECTION
from src.fetch import get_book_text
from src.text import tokenize


def _tfidf_vectors(token_lists, min_df=2, max_df=0.7, top_n=2000):
    n = len(token_lists)
    counts = [Counter(tokens) for tokens in token_lists]
    df = Counter()
    for count in counts:
        df.update(count.keys())
    vocab = {word: d for word, d in df.items() if min_df <= d <= max_df * n}

    vectors = []
    for count in counts:
        weights = {
            word: (1 + math.log(freq)) * math.log(n / vocab[word])
            for word, freq in count.items()
            if word in vocab
        }
        top = sorted(weights.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
        vectors.append(dict(top))
    return vectors


def _cosine(a, b):
    dot = sum(a[word] * b[word] for word in a.keys() & b.keys())
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


def _style_vectors(token_lists, n_words=150):
    counts = [Counter(tokens) for tokens in token_lists]
    total = Counter()
    for count in counts:
        total.update(count)
    vocab = [word for word, _ in total.most_common(n_words)]

    freqs = []
    for count in counts:
        length = sum(count.values()) or 1
        freqs.append([count[word] / length for word in vocab])

    m = len(freqs)
    means = [sum(row[j] for row in freqs) / m for j in range(len(vocab))]
    stds = [
        (sum((row[j] - means[j]) ** 2 for row in freqs) / m) ** 0.5
        for j in range(len(vocab))
    ]
    return [
        [(row[j] - means[j]) / stds[j] if stds[j] else 0.0 for j in range(len(vocab))]
        for row in freqs
    ]


def _delta(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def _corpus_vectors(book_id, build):
    book_id = int(book_id)
    ids = list(COLLECTION) + ([book_id] if book_id not in COLLECTION else [])
    vectors = dict(zip(ids, build([tokenize(get_book_text(i)) for i in ids])))
    return book_id, vectors


def _rank(book_id, vectors, score, reverse, k):
    target = vectors[book_id]
    ranked = sorted(
        (i for i in COLLECTION if i != book_id),
        key=lambda i: score(target, vectors[i]),
        reverse=reverse,
    )
    return [COLLECTION[i][0] for i in ranked[:k]]


def similar(book_id, k=5):
    book_id, vectors = _corpus_vectors(book_id, _tfidf_vectors)
    return _rank(book_id, vectors, _cosine, reverse=True, k=k)


def style_similar(book_id, k=5):
    book_id, vectors = _corpus_vectors(book_id, _style_vectors)
    return _rank(book_id, vectors, _delta, reverse=False, k=k)
