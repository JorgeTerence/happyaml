import re

from yaml import serialize

from backend import build_tree

YamlValue = str | int | float | bool | None


def _escape_quotes(meta_str: str) -> str:
    match = re.search(
        r"(?!\")(?:[^\"\\]|\\.)*(?=\"$)|(?!')(?:[^'\\]|\\.)*(?='$)", meta_str
    )
    if match is None:
        return meta_str

    return match.group()


def _get_inline_value(leaf: str) -> YamlValue:
    """Parses a YAML assigmemt into a Python value."""

    # remove key and separator from line
    val = re.split(r"^\s*.+(?=['\" ]?:\s):|^\s*-\s*", leaf)[-1].strip()

    # try into bool
    if val.lower() in ["true", "y", "yes"]:
        return True
    if val.lower() in ["false", "n", "no"]:
        return False

    # try into null
    if val.lower() in ["null", "~"]:
        return None

    # try into int
    if val.isdecimal():
        return int(val)

    # try into float
    try:
        return float(val)

    # it's string
    except ValueError:
        return _escape_quotes(val)
    ...


def _get_inline_key(leaf: str) -> str: ...


def _serialize(branch: list[str | dict]) -> list[YamlValue] | dict[str, YamlValue]: ...


def _serialize_list(branch: list[str | dict]) -> list[YamlValue]: ...

# idea: convert dicts to plain tuples for nested data


def _serialize_object(branch: list[str | dict[str, list]]) -> dict[str, YamlValue]:
    object = {}

    for sub_branch in branch:
        if type(sub_branch) is str:
            object[_get_inline_key(sub_branch)] = _get_inline_value(sub_branch)
        elif type(sub_branch) is dict:
            key, values = tuple(sub_branch.items())[0]
            object[key.strip().removesuffix(":")] = serialize(values)
    
    return object


def parse(file_name: str) -> list | dict:
    """Reads a YAML file at the specified path and converts it into a Python value, be it a `dict` or a `list`."""
    with open(file_name) as f:
        lines = [
            # remove comments after assignments (i.e. everything after a # outside quotes)
            re.split(r"\s#[^\"|'|\n]+$", l)[0]
            for l in f.readlines()
            # remove blank and comment-only lines
            if re.search(r"^\s*#|^\s*$", l) is None
        ]
        tree = build_tree(lines)
        return _serialize(tree)


def parse_yaml(file_content: str) -> list | dict:
    """Converts the provided YAML content to a Python value."""
    lines = [
        re.split(r"\s#[^\"|'|\n]+$", l)[0]
        for l in file_content.split("\n")
        if re.search(r"^\s*#|^\s*$", l) is None
    ]
    tree = build_tree(lines)
    return _serialize(tree)
