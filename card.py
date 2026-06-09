from tools import get_info
from lexdiv import lexdiv
from entities import entities
from topics import topics
from summarize import summarize
from similar import similar


def card(book_id):
    return {
        "info": get_info(book_id),
        "lexdiv": lexdiv(book_id),
        "topics": topics(book_id),
        "entities": entities(book_id),
        "summary": summarize(book_id),
        "similar": similar(book_id),
    }