import argparse
import csv


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bookworm tools")
    parser.add_argument("--info", type=int, help="Show book info by ID")
    
    args = parser.parse_args()
    
    if args.info is not None:
        print(get_info(args.info))