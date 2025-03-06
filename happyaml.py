import re
from typing import Any

from backend import build_tree
from happyaml2 import _escape_quotes, _get_inline_value


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


def serialize(tree: list[str | dict]) -> dict[str, Any] | list:
    if any(re.search(r"^\s*-", b) is not None for b in tree if type(b) is str):
        return serialize_list(tree)

    return serialize_obj(tree)


def serialize_obj(tree: list[str | dict]) -> dict[str, Any]:
    obj = {}

    for branch in tree:
        # inline value
        if type(branch) is str:
            key = re.search(r"(?!\s).+(?=:\s['\" ]?)", branch).group()  # type: ignore
            if re.search(r"^['\"]", key) is not None:
                key = _escape_quotes(key)

            obj[key] = _get_inline_value(branch)

        # nested value
        elif type(branch) is dict:
            k, v = list(branch.items())[0]
            obj[k.strip().replace(":", "")] = serialize(v)

    return obj


def serialize_list(tree: list[str | dict]) -> list[Any]:
    arr = []
    for branch in tree:
        if type(branch) is str:
            arr.append(_get_inline_value(branch))
        else:
            print("list[dict] ->", branch)
    return arr
