import argparse
from lexdiv import lexdiv


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bookworm NLP engine")
    parser.add_argument("--lexdiv", type=int, help="Lexical diversity metrics")

    args = parser.parse_args()

    if args.lexdiv is not None:
        print(lexdiv(args.lexdiv))