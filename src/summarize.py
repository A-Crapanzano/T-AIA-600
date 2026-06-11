import re

from src.fetch import cached, get_book_text
from src.similar import _cosine, _tfidf_vectors
from src.text import tokenize

_SENTENCE_RE = re.compile(r"[^.!?]+[.!?]")


def _split_sentences(text):
    text = " ".join(text.split())
    sentences = (s.strip() for s in _SENTENCE_RE.findall(text))
    return [s for s in sentences if len(s.split()) >= 4]


def _build_graph(vectors, threshold=0.1):
    n = len(vectors)
    graph = [{} for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            sim = _cosine(vectors[i], vectors[j])
            if sim > threshold:
                graph[i][j] = sim
                graph[j][i] = sim
    return graph


def _pagerank(graph, damping=0.85, iterations=30):
    n = len(graph)
    score = [1.0 / n] * n
    out_weight = [sum(neighbors.values()) for neighbors in graph]
    for _ in range(iterations):
        new = [(1 - damping) / n] * n
        for j in range(n):
            if out_weight[j] == 0:
                continue
            share = damping * score[j] / out_weight[j]
            for i, weight in graph[j].items():
                new[i] += share * weight
        score = new
    return score


@cached
def summarize(book_id, k=5):
    sentences = _split_sentences(get_book_text(book_id))
    vectors = _tfidf_vectors([tokenize(s) for s in sentences])
    scores = _pagerank(_build_graph(vectors))
    top = sorted(range(len(sentences)), key=lambda i: scores[i], reverse=True)[:k]
    return " ".join(sentences[i] for i in sorted(top))
