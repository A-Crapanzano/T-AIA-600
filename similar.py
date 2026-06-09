from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from tools import download_book, clean_gutenberg_text


CORPUS = {
    11: "Alice's Adventures in Wonderland",
    12: "Through the Looking-Glass",
    16: "Peter Pan",
    55: "The Wonderful Wizard of Oz",
    113: "The Secret Garden",
    120: "Treasure Island",
    236: "The Jungle Book",
    108: "The Return of Sherlock Holmes",
    834: "The Memoirs of Sherlock Holmes",
    863: "The Mysterious Affair at Styles",
    1661: "The Adventures of Sherlock Holmes",
    61262: "Poirot Investigates",
    69087: "The Murder of Roger Ackroyd",
    70114: "The Big Four",
    35: "The Time Machine",
    36: "The War of the Worlds",
    84: "Frankenstein; Or, The Modern Prometheus",
    159: "The Island of Doctor Moreau",
    164: "Twenty Thousand Leagues under the Sea",
    345: "Dracula",
    68283: "The Call of Cthulhu",
}


def load_book_text(book_id):
    """Télécharge un livre et renvoie son texte nettoyé."""
    path = download_book(book_id)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return clean_gutenberg_text(text)


def similar(book_id):
    """Renvoie les 5 livres les plus similaires au livre donné."""
    ids = list(CORPUS.keys())
    texts = [load_book_text(bid) for bid in ids]

    vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=2000,
    min_df=2,
    max_df=0.8,
)
    matrix = vectorizer.fit_transform(texts)

    target_index = ids.index(book_id)

    similarities = cosine_similarity(matrix[target_index], matrix).flatten()

    sorted_indices = similarities.argsort()[::-1]

    result = []
    for idx in sorted_indices:
        if idx == target_index:
            continue
        result.append(CORPUS[ids[idx]])
        if len(result) == 5:
            break

    return result