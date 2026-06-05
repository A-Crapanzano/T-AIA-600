import argparse
import csv
import os
import requests
import spacy

_nlp = None


def get_nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load("en_core_web_sm")
    return _nlp

def get_info(book_id):
    with open("data/pg_catalog.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Text#"] == str(book_id):
                return {
                    "id": row["Text#"],
                    "title": row["Title"],
                    "authors": row["Authors"],
                    "bookshelves": row["Bookshelves"],
                }
    return None


def download_book(book_id):
    os.makedirs("books", exist_ok=True)
    path = f"books/{book_id}.txt"

    if os.path.exists(path):
        return path

    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    response = requests.get(url)
    response.raise_for_status()

    with open(path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return path


def clean_gutenberg_text(text):
    start_marker = "*** START"
    end_marker = "*** END"

    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index == -1 or end_index == -1:
        return text

    start_index = text.find("\n", start_index) + 1
    return text[start_index:end_index].strip()


def get_book_tokens(book_id):
    path = download_book(book_id)

    with open(path, encoding="utf-8") as f:
        text = f.read()

    text = clean_gutenberg_text(text)
    doc = get_nlp()(text)
    return [token.text.lower() for token in doc if token.is_alpha]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bookworm tools")
    parser.add_argument("--info", type=int, help="Show book info by ID")
    parser.add_argument("--download", type=int, help="Download book text by ID")

    args = parser.parse_args()

    if args.info is not None:
        print(get_info(args.info))

    if args.download is not None:
        path = download_book(args.download)
        print(f"Book saved to {path}")