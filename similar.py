from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from tools import download_book, clean_gutenberg_text


# Notre annuaire des 21 livres du corpus du sujet
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
    # Étape 2 : charger les textes des 21 livres
    ids = list(CORPUS.keys())
    texts = [load_book_text(bid) for bid in ids]

    # Étape 3 : vectoriser tout le corpus en TF-IDF
    vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=2000,
    min_df=2,
    max_df=0.8,
)
    matrix = vectorizer.fit_transform(texts)

    # Étape 4 : trouver la position du livre cible dans la liste
    target_index = ids.index(book_id)

    # Étape 5 : calculer la similarité avec tous les autres
    similarities = cosine_similarity(matrix[target_index], matrix).flatten()

    # Étape 6 : trier les indices par similarité décroissante
    sorted_indices = similarities.argsort()[::-1]

    # Étape 7 : extraire les 5 meilleurs titres (en excluant le livre cible)
    result = []
    for idx in sorted_indices:
        if idx == target_index:
            continue
        result.append(CORPUS[ids[idx]])
        if len(result) == 5:
            break

    return result