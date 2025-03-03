from math import gcd
import re
from typing import Any


def parse(file_name: str) -> dict:
    with open(file_name) as f:
        lines = [
            l.replace("\n", "")
            for l in f.readlines()
            if not (l.startswith("#") or l.isspace())
        ]

        document_indentation = gcd(*[indentation(l) for l in lines])

        tree = build_tree(lines, document_indentation)

        print("------")
        for branch in tree:
            print(branch)

        return {}


def build_tree(lines: list[str], indent: int) -> list:
    # Assumes the root object is not a list???
    # TODO: account for array items
    # TODO: don't allow for mixed key-value pairs and array elements
    # TODO: validate string quotes
    base_indent = indentation(lines[0] if lines else "")
    layer = []
    for i, line in enumerate(lines):
        if is_nested(line, base_indent):
            continue

        if is_inline(line):
            print("[inline]", line)
            layer.append(line)
        else:
            print("[nested]", line)
            layer.append(
                {line: build_tree(lines[i + 1 : find_next_block_end(lines)], indent)}
            )

    return layer


def is_nested(line: str, indent: int) -> bool:
    return indentation(line) > indent


def is_inline(line) -> bool:
    return re.search(r"(:\s?\S+$)|(^\s*-)", line) is not None


def find_next_block_end(lines: list[str]) -> int:
    base = indentation(lines[0])
    for i, line in enumerate(lines[1:], 1):
        if indentation(line) < base:
            return i

    return len(lines)


def indentation(line: str) -> int:
    return len(re.search(r"^\s*", line).group())  # type: ignore


def serialize(tree: list[str | dict]) -> dict[str, Any]: ...
