import yaml


def test_parse_nested():
    expected = {"root": 1, "branch": {"prop": 2, "arr": [1, 10, 100]}}
    assert yaml.parse("samples/1-simple.yaml") == expected


def test_strings():
    expected = {
        "simple": "hello world",
        "single": "my mom",
        "double": "muscle man",
        "mixed": "how do you spell 'camel'?",
        "mixed2": 'how about "dromedaire"?',
    }
    assert yaml.parse("samples/2-strings.yaml") == expected


def test_comments():
    expected = {"key": "value"}
    assert yaml.parse("samples/3-comments.yaml") == expected
