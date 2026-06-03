from tools import download_book


def clean_gutenberg_text(text):
    start_marker = "*** START"
    end_marker = "*** END"

    start_index = text.find(start_marker)
    end_index = text.find(end_marker)

    if start_index == -1 or end_index == -1:
        return text

    start_index = text.find("\n", start_index) + 1

    return text[start_index:end_index].strip()


def lexdiv(book_id):
    path = download_book(book_id)

    with open(path, encoding="utf-8") as f:
        text = f.read()

    text = clean_gutenberg_text(text)

    print(text[:500])


if __name__ == "__main__":
    lexdiv(11)