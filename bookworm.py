import argparse
import json
from lexdiv import lexdiv
from entities import entities
from similar import similar
from summarize import summarize
from topics import topics

def print_json(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bookworm NLP engine")
    parser.add_argument("--lexdiv", type=int, help="Lexical diversity metrics")
    parser.add_argument("--entities", type=int, help="Extract characters and locations")
    parser.add_argument("--similar", type=int, help="Find 5 most similar books")
    parser.add_argument("--summarize", type=int, help="Summarize a book")
    parser.add_argument("--topics", type=int, help="Extract main topics")


    args = parser.parse_args()

    if args.lexdiv is not None:
        print_json(lexdiv(args.lexdiv))

    if args.entities is not None:
        print_json(entities(args.entities))

    if args.similar is not None:
        print_json(similar(args.similar))
        
    if args.summarize is not None:
        print_json(summarize(args.summarize))
        
    if args.topics is not None:
        print_json(topics(args.topics))