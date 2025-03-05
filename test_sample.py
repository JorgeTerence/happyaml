import happyaml


def test_parse_nested():
    expected = {
        "root": 1,
        "branch": {
            "prop": 2,
            "arr": [1, 10, 100],
            "nested": [2, 20, 200],
        },
        "last": "here"
    }
    assert happyaml.parse("samples/1-simple.yaml") == expected


def test_strings():
    expected = {
        "simple": "hello world",
        "single": "my mom",
        "double": "muscle man",
        "mixed": "how do you spell 'camel'?",
        "mixed2": 'how about "dromedaire"?',
    }
    assert happyaml.parse("samples/2-strings.yaml") == expected


def test_comments():
    expected = {
        "key": "value",
        "chave": "value# this is not a comment",
        "tricky": "why does tick-tack-toes have a # grid and not a ##?",
    }
    assert happyaml.parse("samples/3-comments.yaml") == expected


def test_types():
    expected = {
        "boolean": True,
        "unboolean": False,
        "float": 3.14159,
        "int": 1,
        "string": "one must imagine sysiphus happy",
        "strong": ":3",
        "nope": None,
    }
    assert happyaml.parse("samples/4-types.yaml") == expected


def test_keys():
    expected = {
        "bad design": True,
        "1": "oh no",
        "snake-case": "bleh",
        "quoted": True,
        "single_quoted": "perhaps",
        ":/": "this sucks",
    }
    assert happyaml.parse("samples/5-keys.yaml") == expected


def test_root_list():
    expected = ["VSCode", "IntelliJ", "Micro"]
    assert happyaml.parse("samples/6-root-list.yaml") == expected


def test_dict_list():
    expected = {
        "font_size": 11,
        "indent_size": 4,
        "plugins": [
            {"id": "python", "version": 3.12},
            {"id": "ts", "version": 5.8},
            {"id": "rust", "version": 1.84},
        ],
    }
    assert happyaml.parse("samples/7-list-of-dict.yaml") == expected
