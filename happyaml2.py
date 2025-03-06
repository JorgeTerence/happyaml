import re


YamlValue = str | int | float | bool | None


def parse(file_name: str) -> list | dict:
    """
    Reads a YAML file at the specified path and converts it into a Python value, be it a `dict` or a `list`.
    """
    ...


def parse_yaml(file_content: str) -> list | dict:
    """
    Converts the provided YAML content to a Python value.
    """
    ...


def _build_tree(lines: list[str]) -> list:
    """
    Creates an intermediary representation of the data. Assignmnents are classified as nested or inline.
    All lines of the original document remain in the tree, though get organized in a recursive structure.

    - **Inline** data is what actually caries information. Are plain string values in an `list`;
    - **Nested** data defines structure. Are represented as a `dict` with the label line as the key and children as the nested tree value.
    """

    if len(lines) == 0:
        return []

    branch_indentation = _get_indentation(lines[0])

    return [
        (
            line
            if _is_inline(line)
            # constructs subtree with all nested branches
            else {
                line: _build_tree(
                    lines[i + 1 : _get_branch_limit(lines, i, branch_indentation)]
                )
            }
        )
        for i, line in enumerate(lines)
        if _get_indentation(line) == branch_indentation
    ]
    ...


# =======================


def _get_indentation(line: str) -> int:
    match = re.search(r"^\s+", line)
    if match is None:
        return 0

    return len(match.group())


def _is_inline(line: str) -> bool:
    return (
        # checks if there's anything after the ':' key-value separator
        # accounts for arbitrary string keys
        re.search(r"(?!:\s?)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')|(\w\s?)+$", line)
        is not None
    )


def _get_branch_limit(lines: list[str], root_index: int, indentation: int) -> int:
    # if indentation == 0:
    #     return len(lines)

    for i, line in enumerate(lines[root_index + 1 :], root_index + 1):
        if _get_indentation(line) <= indentation:
            return i

    return len(lines)


# =======================


def _get_inline_value(leaf: str) -> YamlValue:
    """
    Parses a YAML statement into a Python value.
    """
    ...
