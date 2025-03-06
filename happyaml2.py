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
    Creates a mid-level representation of the data. Assignmnents are classified as nested or inline.
    All lines of the original document remain in the tree, though get organized in a recursive structure.

    - **Inline** data is what actually caries information. Are plain string values in an `list`;
    - **Nested** data defines structure. Are represented as a `dict` with the label line as the key and children as the nested tree value.
    """
    ...


def _get_inline_value(leaf: str) -> YamlValue:
    """
    Parses a YAML statement into a Python value.
    """
    ...
