import argparse
import csv
import os
import requests


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

    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    response = requests.get(url)
    response.raise_for_status()

    with open(path, "w", encoding="utf-8") as f:
        f.write(response.text)

    return path


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