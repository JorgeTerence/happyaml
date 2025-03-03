from math import gcd
import re
from typing import Any


def parse(file_name: str) -> dict:
    with open(file_name) as f:
        lines = f.readlines()

        document_indentation = gcd(*[len(re.search(r"^\s*", l).group()) for l in lines])  # type: ignore

        tree = build_tree(lines, document_indentation)
        print(tree)
        return {}


def build_tree(lines: list[str], indent: int) -> list:
    # Assumes the root object is not a list
    layer = []
    for i, line in enumerate(lines):
        if is_nested(line):
            continue

        # TODO: account for array items
        if is_inline(line):
            layer.append(line)
        else:
            # DECIDE: define block bounds here or in the loop?
            nested_block_end = find_next_block_end(lines)
            layer.append({line: build_tree(lines[i:nested_block_end], indent)})

    return layer


def is_nested(line) -> bool: ...

def is_inline(line) -> bool: ...

def find_next_block_end(lines: list[str]) -> int: ...


def serialize(tree: list[str | dict]) -> dict[str, Any]: ...
