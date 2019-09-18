#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from docopt import docopt

from xortool.charset import get_charset


class ArgError(Exception):
    pass


def parse_char(ch):
    """
    'A' or '\x41' or '0x41' or '41'
    '\x00' or '0x00' or '00'
    """
    if ch is None:
        return None
    if len(ch) == 1:
        return bytes([ord(ch)])
    if ch[0:2] in ("0x", "\\x"):
        ch = ch[2:]
    if not ch:
        raise ValueError("Empty char")
    if len(ch) > 2:
        raise ValueError("Char can be only a char letter or hex")
    return bytes([int(ch, 16)])


def parse_parameters(doc, version):
    p = docopt(doc, version=version)
    p = {k.lstrip("-"): v for k, v in p.items()}
    try:
        return {
            "input_is_hex": bool(p["hex"]),
            "max_key_length": int(p["max-keylen"]),
            "known_key_length": int(p["key-length"]) if p["key-length"] else None,
            "most_frequent_char": parse_char(p["char"]),
            "brute_chars": bool(p["brute-chars"]),
            "brute_printable": bool(p["brute-printable"]),
            "text_charset": get_charset(p["text-charset"]),
            "frequency_spread": 0,  # to be removed
            "filename": p["FILE"] if p["FILE"] else "-",  # stdin by default
            "filter_output": bool(p["filter-output"]),
        }
    except ValueError as err:
        raise ArgError(str(err))
