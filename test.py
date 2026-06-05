from similar import load_book_text, CORPUS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ids = list(CORPUS.keys())
texts = [load_book_text(bid) for bid in ids]

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000,
    min_df=2,
    max_df=0.95,
    ngram_range=(1, 2),
    sublinear_tf=True,
)
matrix = vectorizer.fit_transform(texts)

target_index = ids.index(11)
sims = cosine_similarity(matrix[target_index], matrix).flatten()

pairs = sorted(
    [(sims[i], CORPUS[ids[i]]) for i in range(len(ids))],
    reverse=True,
)

for score, title in pairs:
    print(f"{score:.4f}  {title}")