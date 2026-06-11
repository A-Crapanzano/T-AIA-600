from src.entities import entities
from src.fetch import get_book_info, get_book_text
from src.lexdiv import lexdiv
from src.similar import similar
from src.summarize import summarize
from src.topics import topics


def card(book_id):
    text = get_book_text(book_id)
    return {
        "info": get_book_info(book_id),
        "lexdiv": lexdiv(text),
        "topics": topics(text),
        "entities": entities(book_id),
        "summary": summarize(book_id),
        "similar": similar(book_id),
    }
