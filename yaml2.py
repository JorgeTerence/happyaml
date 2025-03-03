from math import gcd
import re
from typing import Any


def parse(file_name: str) -> dict | list:
    with open(file_name) as f:
        lines = [
            l.replace("\n", "")
            for l in f.readlines()
            if not (l.startswith("#") or l.isspace())
        ]

        document_indentation = gcd(*[indentation(l) for l in lines])

        tree = build_tree(lines, document_indentation)

        return serialize(tree)


def build_tree(lines: list[str], indent: int) -> list:
    # Assumes the root object is not a list???
    # TODO: don't allow for mixed key-value pairs and array elements
    base_indent = indentation(lines[0] if lines else "")
    layer = []
    for i, line in enumerate(lines):
        if is_nested(line, base_indent):
            continue

        if is_inline(line):
            layer.append(line)
        else:
            layer.append(
                {line: build_tree(lines[i + 1 : sub_block_bound(lines)], indent)}
            )

    return layer


def is_nested(line: str, indent: int) -> bool:
    return indentation(line) > indent


def is_inline(line) -> bool:
    return (
        re.search(r"(?!:\s?)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')|(\w\s?)+$", line)
        # (?!")(?:[^"\\]|\\.)*(?="$)|(?!')(?:[^'\\]|\\.)*(?='$)
        is not None
    )


def sub_block_bound(lines: list[str]) -> int:
    base = indentation(lines[0])
    for i, line in enumerate(lines[1:], 1):
        if indentation(line) < base:
            return i

    return len(lines)


def indentation(line: str) -> int:
    return len(re.search(r"^\s*", line).group())  # type: ignore


def get_inline_value(branch: str) -> str | int | float:
    val = re.search(r'(?!:\s?)[(\s?\w+)|"|\']+$', branch).group().strip()  # type: ignore

    # if it's a quoted string:
    if re.search(r"^['\"]", val) is not None:
        # escape quotes
        return re.search(r"(?!\")(?:[^\"\\]|\\.)*(?=\"$)|(?!')(?:[^'\\]|\\.)*(?='$)", val).group()  # type: ignore
    # try into int
    elif val.isdecimal():
        return int(val)
    else:
        # try into float
        try:
            return float(val)
        # it's an unquoted string
        except ValueError:
            return val


def serialize(tree: list[str | dict]) -> dict[str, Any] | list:
    if any(b.strip().startswith("-") for b in tree if type(b) == str):
        return serialize_list(tree)

    obj = {}

    for branch in tree:
        # inline value
        if type(branch) == str:
            key = re.search(r"(?!^\s)\w+(?=:)", branch).group()  # type: ignore
            obj[key] = get_inline_value(branch)

        # nested value
        elif type(branch) == dict:
            k, v = list(branch.items())[0]
            obj[k.strip().replace(":", "")] = serialize(v)

    return obj


def serialize_list(tree: list[str | dict]) -> list[Any]:
    arr = []
    for branch in tree:
        if type(branch) == str:
            arr.append(get_inline_value(branch))
        elif type(branch) == dict:
            print("TODO: dict array ->", branch)
            # arr.append(serialize(branch))

    return arr
