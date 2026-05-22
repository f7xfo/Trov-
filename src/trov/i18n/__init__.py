"""Internationalization — Khmer + English message catalogs."""

import json
from pathlib import Path

_catalogs: dict[str, dict[str, str]] = {}
_dir = Path(__file__).parent


def _load(lang: str) -> dict[str, str]:
    if lang not in _catalogs:
        path = _dir / f"{lang}.json"
        with open(path, "r", encoding="utf-8") as f:
            _catalogs[lang] = json.load(f)
    return _catalogs[lang]


def t(key: str, lang: str, **kwargs) -> str:
    """Look up a message by key in the given language, with optional formatting."""
    catalog = _load(lang)
    msg = catalog.get(key, key)
    if kwargs:
        msg = msg.format(**kwargs)
    return msg
