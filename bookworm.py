import argparse
from lexdiv import lexdiv
from entities import entities


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bookworm NLP engine")
    parser.add_argument("--lexdiv", type=int, help="Lexical diversity metrics")
    parser.add_argument("--entities", type=int, help="Extract characters and locations")

    args = parser.parse_args()

    if args.lexdiv is not None:
        print(lexdiv(args.lexdiv))

    if args.entities is not None:
        print(entities(args.entities))