from math import gcd
import re
from typing import Any


def parse(file_name: str) -> dict | list:
    with open(file_name) as f:
        # remove blank and comment-only lines
        lines = [
            re.split(r"\s#[^\"|'|\n]+$", l)[0]
            for l in f.readlines()
            if re.search(r"^\s*#|^\s*$", l) is None
        ]

        tree = build_tree(lines)

        return serialize(tree)


def build_tree(lines: list[str]) -> list:
    block_indent = indentation(lines[0] if lines else "")

    return [
        (
            line
            if is_inline(line)
            else {line: build_tree(lines[i : child_bounds(lines, i)])}
        )
        for i, line in enumerate(lines, 1)
        if indentation(line) == block_indent  # skips nested blocks
    ]


def is_inline(line) -> bool:
    return (
        re.search(r"(?!:\s?)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')|(\w\s?)+$", line)
        is not None
    )


def child_bounds(lines: list[str], root_index: int) -> int:
    indent = indentation(lines[0])
    if indent == 0:
        return len(lines)

    for i, line in enumerate(lines[2:], 1):
        if indentation(line) == indent:
            return i + root_index

    return len(lines)


# DONE
def indentation(line: str) -> int:
    return len(re.search(r"^\s*", line).group())  # type: ignore


def escape_quotes(meta_str: str) -> str:
    return re.search(r"(?!\")(?:[^\"\\]|\\.)*(?=\"$)|(?!')(?:[^'\\]|\\.)*(?='$)", meta_str).group()  # type: ignore


def get_inline_value(branch: str) -> str | int | float | bool | None:
    val = re.split(r"^\s*.+(?=['\" ]?:\s):|^\s*-\s*", branch)[-1].strip()  # type: ignore

    # try into bool
    if val.lower() in ["true", "y", "yes"]:
        return True
    if val.lower() in ["false", "n", "no"]:
        return False
    # try into null
    if val.lower() in ["null", "~"]:
        return None
    # try into quoted string
    if re.search(r"^['\"]", val) is not None:
        return escape_quotes(val)
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
    if any(re.search(r"^\s*-", b) is not None for b in tree if type(b) is str):
        return serialize_list(tree)

    return serialize_obj(tree)


def serialize_obj(tree: list[str | dict]) -> dict[str, Any] | list:
    obj = {}

    for branch in tree:
        # inline value
        if type(branch) is str:
            key = re.search(r"(?!\s).+(?=:\s['\" ]?)", branch).group()  # type: ignore
            if re.search(r"^['\"]", key) is not None:
                key = escape_quotes(key)

            obj[key] = get_inline_value(branch)

        # nested value
        elif type(branch) is dict:
            k, v = list(branch.items())[0]
            obj[k.strip().replace(":", "")] = serialize(v)

    return obj


def serialize_list(tree: list[str | dict]) -> list[Any]:
    arr = []
    for branch in tree:
        if type(branch) is str:
            arr.append(get_inline_value(branch))
        else:
            print("list[dict] ->", branch)
    return arr
