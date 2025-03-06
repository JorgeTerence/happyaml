import re


def _get_indentation(line: str) -> int:
    match = re.search(r"^\s+", line)
    if match is None:
        return 0

    return len(match.group())


def _is_inline(line: str) -> bool:
    """Checks for any value after the double-colon `':'` separator. Accounts for arbitrary string keys."""

    return (
        re.search(r"(?!:\s?)(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')|(\w\s?)+$", line)
        is not None
    )


def _get_branch_limit(lines: list[str], root_index: int, indentation: int) -> int:
    """Read it as *"within `lines`, the branch starting at line `root_index` with indentation at `indentation` ends at `_get_branch_limit(...) - 1`"*."""

    for i, line in enumerate(lines[root_index + 1 :], root_index + 1):
        if _get_indentation(line) <= indentation:
            return i

    return len(lines)


def build_tree(lines: list[str]) -> list[str | tuple[str, list]]:
    """
    Creates an intermediary representation of the data. Assignmnents are classified as nested or inline.
    All lines of the original document remain in the tree, though get organized in a recursive structure.

    - **Inline** data is what actually caries information. Are plain string values in an `list`;
    - **Nested** data defines structure. Are represented as a `dict` with the label line as the key and children as the nested tree value.
    """

    if len(lines) == 0:
        return []

    branch_indentation = _get_indentation(lines[0])
    list_mode = re.search(r"^\s*-", lines[0]) is not None

    # if not list_mode, filter for exact indentation
    # else filter for exact on first and exact or +2 on others

    print(lines)
    print([line for line in lines if _get_indentation(line) == branch_indentation])
    print(list_mode)

    tree = []

    for i, line in enumerate(lines):
        line_indentation = _get_indentation(line)
        if line_indentation != branch_indentation:
            continue
    
        if _is_inline(line):
            tree.append(line)
        else:
            tree.append((line, build_tree(lines[i+1: _get_branch_limit(lines, i, branch_indentation)])))

    return tree
