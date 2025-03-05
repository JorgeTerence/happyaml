from math import gcd
import re
from typing import Any


def parse(file_name: str) -> dict | list:
    with open(file_name) as f:
        lines = [
            l.split("#")[0]
            for l in f.readlines()
            if not (l.startswith("#") or l.isspace())
        ]

        document_indentation = gcd(*[indentation(l) for l in lines])

        tree = build_tree(lines, document_indentation)

        return serialize(tree)


def build_tree(lines: list[str], indent: int) -> list:
    # TODO: allow for list root
    # TODO: don't allow for mixed key-value pairs and array elements
    block_indent = indentation(lines[0] if lines else "")

    # return [
    #     line if is_inline(line)
    #     else {line: build_tree(lines[i + 1 : sub_block_bound(lines)], indent)}
    #     for i, line in enumerate(lines)    
        
    #     # skips nested blocks
    #     if indentation(line) > block_indent
    # ]

    layer = []
    for i, line in enumerate(lines):
        # skips nested blocks
        if indentation(line) > block_indent:
            continue

        if is_inline(line):
            layer.append(line)
        else:
            layer.append(
                {line: build_tree(lines[i + 1 : sub_block_bound(lines)], indent)}
            )

    return layer


def is_inline(line) -> bool:
    return (
        re.search(r"(?!:\s?)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')|(\w\s?)+$", line)
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
    if any(re.search(r"^\s*-", b) is not None for b in tree if type(b) == str):
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

    return arr
