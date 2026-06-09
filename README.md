# 📚 Bookworm — Moteur NLP pour les livres Project Gutenberg

Bookworm est un outil CLI Python qui effectue des analyses NLP sur des livres issus de Project Gutenberg. Il génère des "fiches de livres" structurées contenant des métriques lexicales, une modélisation thématique, de la reconnaissance d'entités nommées, un résumé extractif et des recommandations de livres similaires.

Réalisé dans le cadre du module Epitech T-AIA-600.

---

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/A-Crapanzano/T-AIA-600.git
cd T-AIA-600
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Télécharger le modèle anglais spaCy

```bash
python -m spacy download en_core_web_sm
```

### 5. Télécharger le tokenizer NLTK

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab')"
```

### 6. Télécharger le catalogue CSV Gutenberg

Télécharger le catalogue ici :
https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv

Le placer dans le dossier `data/` à la racine du projet.

---

## 📁 Structure du projet

```
T-AIA-600/
├── bookworm.py       # Point d'entrée principal (CLI)
├── tools.py          # Téléchargement, nettoyage, tokenisation
├── lexdiv.py         # Métriques de diversité lexicale
├── entities.py       # Reconnaissance d'entités nommées (NER)
├── similar.py        # Similarité entre livres (TF-IDF + cosinus)
├── summarize.py      # Résumé extractif (LexRank)
├── topics.py         # Modélisation thématique (LDA)
├── card.py           # Agrégateur de fiche complète
├── data/
│   └── pg_catalog.csv
├── books/            # Textes téléchargés (généré automatiquement)
├── requirements.txt
└── README.md
```

---

## 🛠️ Utilisation

Toutes les commandes suivent ce schéma :

```bash
python bookworm.py --<option> <id_livre>
```

Où `<id_livre>` est l'identifiant Project Gutenberg (ex: `11` pour Alice au Pays des Merveilles).

### `--info` — Métadonnées du livre

```bash
python tools.py --info 11
```

Retourne un dictionnaire avec l'id, le titre, les auteurs et les rayons.

### `--download` — Télécharger un livre

```bash
python tools.py --download 11
```

Télécharge le livre au format texte brut UTF-8 dans le dossier `books/`.

### `--lexdiv` — Diversité lexicale

```bash
python bookworm.py --lexdiv 11
```

Retourne 6 métriques de diversité lexicale :

```json
{
  "tok": 26683,
  "typ": 2551,
  "hap": 1104,
  "ttr": 0.0956,
  "mwl": 4.0,
  "mwf": 10.46
}
```

### `--entities` — Reconnaissance d'entités nommées

```bash
python bookworm.py --entities 11
```

Retourne les personnages et lieux extraits du livre :

```json
{
  "characters": ["Alice", "Bill", "Gryphon", "Hatter", ...],
  "locations": ["Wonderland", "Paris", "Rome", ...]
}
```

### `--topics` — Modélisation thématique

```bash
python bookworm.py --topics 11
```

Retourne les 10 mots les plus représentatifs de chaque topic extrait via LDA :

```json
{
  "1": ["rabbit", "door", "mouse", ...],
  "2": ["queen", "gryphon", "turtle", ...],
  "3": ["hatter", "dormouse", "tea", ...],
  "4": ["king", "duchess", "moral", ...]
}
```

### `--summarize` — Résumé extractif

```bash
python bookworm.py --summarize 11
```

Retourne un résumé court du livre sous forme de quelques phrases.

### `--similar` — Livres similaires

```bash
python bookworm.py --similar 11
```

Retourne les 5 livres les plus similaires du corpus, triés par similarité décroissante :

```json
[
  "Through the Looking-Glass",
  "The Adventures of Sherlock Holmes",
  "Frankenstein; Or, The Modern Prometheus",
  "The War of the Worlds",
  "The Jungle Book"
]
```

### `--card` — Fiche complète

```bash
python bookworm.py --card 11
```

Agrège toutes les analyses en un seul dictionnaire structuré.

---

## 🧠 Méthodologie

### Diversité lexicale (`--lexdiv`)

Calculée directement à partir du texte tokenisé avec spaCy. Les tokens sont filtrés pour ne garder que les tokens de mots alphabétiques. Toutes les métriques sont calculées sur les tokens en minuscules.

**Métriques :** tok, typ, hap, ttr, mwl, mwf.

**Limite :** Le TTR diminue mécaniquement à mesure que la longueur du texte augmente, rendant les comparaisons entre livres peu fiables. Des métriques avancées (MTLD, MATTR) corrigeraient ce biais.

---

### Reconnaissance d'entités nommées (`--entities`)

Utilise le modèle `en_core_web_sm` de spaCy pour détecter les entités nommées. Seuls les labels `PERSON` sont conservés pour les personnages, et `GPE`/`LOC` pour les lieux. Un seuil de fréquence (`min_occurrences=2`) filtre les faux positifs.

**Limite :** Le modèle léger produit des faux positifs sur les textes littéraires (titres de chapitres, mots capitalisés en début de phrase). Un modèle plus grand (`en_core_web_lg`) améliorerait la précision mais dépasse la contrainte légèreté du projet.

---

### Modélisation thématique (`--topics`)

Le livre est découpé en chapitres grâce aux marqueurs `CHAPTER`. Chaque chapitre est lemmatisé et nettoyé avec spaCy, puis vectorisé avec `CountVectorizer`. LDA (`sklearn`) est entraîné avec 4 topics et `random_state=42` pour la reproductibilité.

**Pourquoi LDA plutôt que LSA ?** LDA est un modèle probabiliste qui produit des topics plus interprétables. LSA est plus rapide mais les topics sont plus difficiles à lire.

**Limite :** Le nombre de topics (4) est un choix manuel. Une analyse du score de cohérence permettrait de trouver le nombre optimal automatiquement.

---

### Résumé extractif (`--summarize`)

Utilise la bibliothèque `sumy` avec l'algorithme LexRank. LexRank sélectionne les phrases en fonction de leur similarité avec les autres phrases du texte (approche basée sur les graphes). Testé contre LSA et Luhn — LexRank a produit les résultats les plus lisibles sur les textes littéraires narratifs.

**Limite :** Les méthodes extractives copient les phrases telles quelles. Sans reformulation, certaines phrases manquent de contexte lues isolément. Les méthodes abstractives (BART, T5) produiraient des résumés plus naturels mais sont interdites par les contraintes du projet.

---

### Similarité entre livres (`--similar`)

Les livres sont vectorisés avec TF-IDF (`TfidfVectorizer` avec `ngram_range=(1,2)`, `sublinear_tf=True`). La similarité cosinus est calculée entre le livre cible et les 21 livres du corpus.

**Pourquoi TF-IDF plutôt que les embeddings ?** TF-IDF est léger et tourne en local. Les sentence embeddings (BERT, Sentence-Transformers) captureraient la similarité sémantique plus précisément mais nécessitent des modèles lourds, interdits par le projet.

**Limite :** TF-IDF compare des vocabulaires, pas des sens. Deux livres traitant du même thème avec des vocabulaires différents peuvent avoir un score de similarité faible.

---

## 📦 Corpus de livres

La commande `--similar` fonctionne sur un corpus fixe de 21 livres de Project Gutenberg répartis en 3 genres :

| Genre | Livres |
|---|---|
| Enfants / Jeunes Adultes | Alice, Through the Looking-Glass, Peter Pan, Wizard of Oz, Secret Garden, Treasure Island, Jungle Book |
| Crime, Mystère & Thriller | Sherlock Holmes (x3), Poirot Investigates, Roger Ackroyd, The Big Four, Mysterious Affair at Styles |
| Science-Fiction & Fantasy | Time Machine, War of the Worlds, Frankenstein, Doctor Moreau, 20 000 Lieues, Dracula, Call of Cthulhu |

---

## 📋 Dépendances

- `spacy` + `en_core_web_sm` — Pipeline NLP (tokenisation, lemmatisation, NER)
- `scikit-learn` — Vectorisation TF-IDF, similarité cosinus, LDA
- `sumy` + `nltk` — Résumé extractif
- `requests` — Requêtes HTTP vers Project Gutenberg

---

## 👤 Auteur

Alexandre Crapanzano — Epitech Marseille, MSc Architecte de Systèmes d'Information (2025/2026)
