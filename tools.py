import csv

book_id = 11

with open("data/pg_catalog.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        if row["Text#"] == str(book_id):
            info = {
                "id": row["Text#"],
                "title": row["Title"],
                "authors": row["Authors"],
                "bookshelves": row["Bookshelves"],
            }
            print(info)
            break