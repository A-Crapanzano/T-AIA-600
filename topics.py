from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from tools import download_book, clean_gutenberg_text, get_nlp

NUM_TOPICS = 4
NUM_WORDS = 10
EXTRA_STOPWORDS = [
    "alice", "say", "go", "come", "know", "like",
    "think", "little", "look", "begin", "way", "get"
]


def split_into_chapters(text):
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

    return sections[1:]


def clean_chapter(chapter_text):
    nlp = get_nlp()
    doc = nlp(chapter_text)
    words = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha
        and not token.is_stop
        and len(token) > 2
    ]
    return " ".join(words)


def topics(book_id):
    path = download_book(book_id)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = clean_gutenberg_text(text)

    chapters = split_into_chapters(text)
    chapter_strings = [clean_chapter(chapter) for chapter in chapters]

    vectorizer = CountVectorizer(
        max_features=500,
        stop_words=EXTRA_STOPWORDS,
    )
    matrix = vectorizer.fit_transform(chapter_strings)

    lda = LatentDirichletAllocation(n_components=NUM_TOPICS, random_state=42)
    lda.fit(matrix)

    feature_names = vectorizer.get_feature_names_out()
    result = {}
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [
            feature_names[i]
            for i in topic.argsort()[-NUM_WORDS:][::-1]
        ]
        result[topic_idx + 1] = top_words

    return result