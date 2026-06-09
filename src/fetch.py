import csv
import functools
import http.client
import io
import json
import os
import re
import urllib.request

from loguru import logger

CACHE_DIR = ".bookcache"


def _cache_path(name, args, kwargs):
    parts = [name, *map(str, args)]
    parts += [f"{k}={v}" for k, v in sorted(kwargs.items())]
    key = "_".join(parts) + ".json"
    key = key.replace("/", "_").replace(os.sep, "_")
    return os.path.join(CACHE_DIR, key)


def _json_default(obj):
    if hasattr(obj, "tolist"):
        return obj.tolist()
    if isinstance(obj, (set, frozenset)):
        return list(obj)
    raise TypeError(f"type non sérialisable : {type(obj).__name__}")


def cached(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        path = _cache_path(func.__name__, args, kwargs)
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                pass
        result = func(*args, **kwargs)
        try:
            payload = json.dumps(result, ensure_ascii=False, default=_json_default)
        except TypeError as e:
            logger.warning("Résultat non mis en cache (non sérialisable) : {}", e)
            return result
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            tmp = f"{path}.{os.getpid()}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(payload)
            os.replace(tmp, path)
        except OSError as e:
            logger.warning("Cache non écrit ({}) : {}", path, e)
        return json.loads(payload)

    return wrapper


def _fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (bookworm)"})
    return (
        urllib.request.urlopen(req, timeout=timeout)
        .read()
        .decode("utf-8", errors="replace")
    )


def _strip_boilerplate(raw):
    start = re.search(r"\*\*\* START OF TH(E|IS) PROJECT GUTENBERG.*?\*\*\*", raw)
    end = re.search(r"\*\*\* END OF TH(E|IS) PROJECT GUTENBERG.*?\*\*\*", raw)
    if start and end:
        return raw[start.end() : end.start()].strip()
    raise ValueError("Marqueurs Project Gutenberg introuvables.")


def _header_field(raw, field):
    header = raw.split("*** START", 1)[0]
    values = re.findall(rf"^{field}:\s*(.+)$", header, re.MULTILINE)
    return ", ".join(v.strip() for v in values)


URL_PATTERNS = [
    "https://www.gutenberg.org/cache/epub/{id}/pg{id}.txt",
    "https://www.gutenberg.org/files/{id}/{id}-0.txt",
]


@cached
def _download(book_id):
    errors = []
    for pattern in URL_PATTERNS:
        url = pattern.format(id=book_id)
        try:
            raw = _fetch(url)
            return {
                "text": _strip_boilerplate(raw),
                "title": _header_field(raw, "Title"),
                "author": _header_field(raw, "Author"),
            }
        except (OSError, http.client.IncompleteRead) as e:
            errors.append(f"{url} -> {e}")
        except ValueError as e:
            errors.append(f"{url} -> contenu non exploitable : {e}")
    raise RuntimeError(
        f"Impossible de récupérer le livre {book_id} :\n  " + "\n  ".join(errors)
    )


def get_book_text(book_id):
    return _download(book_id)["text"]


CATALOG_URL = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"


@cached
def _catalog_bookshelves():
    raw = _fetch(CATALOG_URL, timeout=60)
    csv.field_size_limit(10**7)
    reader = csv.DictReader(io.StringIO(raw))
    return {row["Text#"]: row["Bookshelves"] for row in reader if row["Bookshelves"]}


def _get_bookshelves(book_id):
    try:
        catalog = _catalog_bookshelves()
    except (OSError, http.client.IncompleteRead, csv.Error) as e:
        logger.warning("Catalogue Gutenberg indisponible : {}", e)
        return "unknown"
    return catalog.get(str(book_id), "unknown")


def get_book_info(book_id):
    book = _download(book_id)
    return {
        "id": str(book_id),
        "authors": book["author"] or "unknown",
        "bookshelves": _get_bookshelves(book_id),
    }
