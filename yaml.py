import re
from math import gcd

# Alternative idea: instead of passing the entire document, pass the next block -> no need for indent and block_start


def yamler(block: list[str], indent_size: int) -> dict:
    obj = {}
    for i, line in enumerate(block):
        try:
            key = re.search(r"\w+(?=:)", line).string  # type: ignore
        except AttributeError:
            raise KeyError("Failed to parse key in line %d:\n%s", i, line)

        # TODO: don't mess up strings
        if (inline_values := re.search(r"(?!:\s?)\S+$", line)) is not None:
            print("[inline] value =", inline_values.string)
            obj[key] = inline_values
        else:
            print("[nested] key =", key)
            print("line =", line)
            obj[key] = yamler(sub_block(block, indent_size), indent_size)

    return obj


def sub_block(block: list[str], indent_size: int) -> list[str]:
    # start = next line
    # end = earlies line where indentation < current_indentation + indent_size

    print(block[1])
    current_indent = re.match(r"^\s+", block[1]).string  # type: ignore

    for i, line in enumerate(block[1:]):
        if re.match(rf"$\s{{current_index}}", line) is None:
            return block[1:i]

    return block[1:2]


def parse(file_name: str) -> dict:
    with open(file_name) as f:
        document = [l for l in f.readlines() if not (l.startswith("#") or l.isspace())]

        document_indentation = gcd(
            *[
                len(
                    match.string
                    if (match := re.match(r"^\s+", line)) is not None
                    else ""
                )
                for line in document
            ]
        )
        return yamler(document, document_indentation)
