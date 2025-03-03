import re
from math import gcd


def yamler(block: list[str], indent_size: int) -> dict | list:
    arr = []
    obj = {}

    # TODO: skip lines where the indentation is different from the current one
    for i, line in enumerate(block):
        
        try:
            key = re.search(r"\w+(?=:)", line).group()  # type: ignore
        except AttributeError:
            raise KeyError("Failed to parse key in line %d:\n%s" % (i, line))

        # TODO: don't mess up strings
        is_inline = re.search(r":$", line) is None
        if is_inline:
            inline_values = re.search(r"(?!:\s?)\S+$", line)
            print("[inline]")
            print("key =", key)
            print("value =", inline_values.group())  # type: ignore
            obj[key] = inline_values
        else:
            print("[nested] key =", key)
            print("line =", line)

            obj[key] = yamler(sub_block(block[i:], indent_size), indent_size)

    return obj


def sub_block(block: list[str], indent_size: int) -> list[str]:
    # start = next line
    # end = earlies line where indentation < current_indentation + indent_size
    current_indent = re.match(r"^\s+", block[1]).string  # type: ignore

    for i, line in enumerate(block[1:]):
        if re.match(rf"$\s{{current_index}}", line) is None:
            return block[1:i]

    return block[1:2]


def parse(file_name: str) -> dict | list:
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
