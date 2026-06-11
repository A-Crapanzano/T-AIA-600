import argparse
import json
import sys

from src.fetch import get_book_text
from src.card import card
from src.entities import entities
from src.lexdiv import advanced_diversity, lexdiv
from src.similar import similar, style_similar
from src.summarize import summarize
from src.topics import topics

COMMANDS = {
    "lexdiv": lambda book_id: lexdiv(get_book_text(book_id)),
    "topics": lambda book_id: topics(get_book_text(book_id)),
    "entities": lambda book_id: entities(book_id),
    "similar": lambda book_id: similar(book_id),
    "summarize": lambda book_id: summarize(book_id),
    "card": lambda book_id: card(book_id),
}


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="bookworm",
        description="Crée des fiches NLP à partir de livres Project Gutenberg.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    for name in COMMANDS:
        group.add_argument(
            f"--{name}",
            metavar="ID",
            type=int,
            help=f"commande {name} sur le livre <ID>",
        )
    parser.add_argument(
        "--full",
        action="store_true",
        help="avec --lexdiv : ajoute les métriques robustes à la longueur (MATTR, MTLD)",
    )
    parser.add_argument(
        "--style",
        action="store_true",
        help="avec --similar : compare par STYLE (mots-outils) au lieu du thème",
    )
    return parser


def main():
    args = vars(_build_parser().parse_args())
    full = args.pop("full")
    style = args.pop("style")
    name, book_id = next((n, args[n]) for n in COMMANDS if args[n] is not None)

    try:
        if name == "similar" and style:
            result = style_similar(book_id)
        else:
            result = COMMANDS[name](book_id)
            if name == "lexdiv" and full:
                result |= advanced_diversity(get_book_text(book_id))
    except RuntimeError as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
