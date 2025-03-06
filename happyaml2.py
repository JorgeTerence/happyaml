import re


YamlValue = str | int | float | bool | None


def _escape_quotes(meta_str: str) -> str:
    match = re.search(
        r"(?!\")(?:[^\"\\]|\\.)*(?=\"$)|(?!')(?:[^'\\]|\\.)*(?='$)", meta_str
    )
    if match is None:
        return meta_str

    return match.group()


def _get_inline_value(leaf: str) -> YamlValue:
    """Parses a YAML statement into a Python value."""

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


def serialize(branch: list[str | dict]) -> list[YamlValue] | dict[str, YamlValue]: ...


def serialize_list(branch: list[str | dict]) -> list[YamlValue]: ...


def serialize_object(branch: list[str | dict]) -> dict[str, YamlValue]: ...


def parse(file_name: str) -> list | dict:
    """Reads a YAML file at the specified path and converts it into a Python value, be it a `dict` or a `list`."""
    ...


def parse_yaml(file_content: str) -> list | dict:
    """Converts the provided YAML content to a Python value."""
    ...
