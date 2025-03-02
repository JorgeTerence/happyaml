import re
from math import gcd

# Alternative idea: instead of passing the entire document, pass the next block -> no need for indent and block_start


def yamler(doc: list[str], indent_size: int, indent: int, block_start: int) -> dict:
    obj = {}
    for line in doc[block_start:]:
        if line.isspace():
            continue

        print("debug loop")
        if len(re.match(r"\s\{%s}" % indent_size, line) or ""):
            break

        key = ""
        if (match := re.match(r"\w+(?=:)", line)) is not None:
            key = match.string
        else:
            print("no key")
            print(line)
            return {}
            # raise Exception("no key")

        if (inline_values := re.match(r"(?!:\s?)\S+$", line)) is not None:
            print("debug inline")
            print(inline_values.string)
        else:
            print("debug nested")
            obj[key] = yamler(doc, indent_size, indent + indent_size, block_start + 1)
            inline_values = match.string

        block_start += 1

    return obj


def parse(file_name: str) -> dict:
    with open(file_name) as f:
        document = f.readlines()
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
        return yamler(document, document_indentation, 0, 0)
