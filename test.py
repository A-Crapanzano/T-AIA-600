from tools import download_book, clean_gutenberg_text, get_nlp
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

path = download_book(11)
with open(path, encoding="utf-8") as f:
    text = f.read()
text = clean_gutenberg_text(text)

sections = []
current_section = []
for line in text.split("\n"):
    if line.startswith("CHAPTER"):
        if current_section:
            sections.append("\n".join(current_section))
        current_section = []
    else:
        current_section.append(line)
if current_section:
    sections.append("\n".join(current_section))
chapters = sections[1:]

nlp = get_nlp()
cleaned_chapters = []
for chapter in chapters:
    doc = nlp(chapter)
    clean_words = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha
        and not token.is_stop
        and len(token) > 2
    ]
    cleaned_chapters.append(clean_words)

chapter_strings = [" ".join(chapter) for chapter in cleaned_chapters]

EXTRA_STOPWORDS = ["alice", "say", "go", "come", "know", "like", "think", "little", "look", "begin", "way"]

vectorizer = CountVectorizer(
    max_features=500,
    stop_words=EXTRA_STOPWORDS,
)

# ← ligne manquante !
matrix = vectorizer.fit_transform(chapter_strings)

lda = LatentDirichletAllocation(n_components=4, random_state=42)
lda.fit(matrix)

print(f"Taille de la matrice : {matrix.shape}")
print(f"LDA entraîné ! Nombre de topics : {lda.n_components}")

feature_names = vectorizer.get_feature_names_out()
for topic_idx, topic in enumerate(lda.components_):
    top_words = [feature_names[i] for i in topic.argsort()[-10:][::-1]]
    print(f"Topic {topic_idx + 1} : {top_words}")