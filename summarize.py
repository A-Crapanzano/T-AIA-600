from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


from tools import download_book, clean_gutenberg_text

SENTENCES_COUNT = 5


def summarize(book_id):
    path = download_book(book_id)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    text = clean_gutenberg_text(text)

    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    summarizer = LexRankSummarizer()
    summary_sentences = summarizer(parser.document, SENTENCES_COUNT)

    return " ".join(str(sentence) for sentence in summary_sentences)