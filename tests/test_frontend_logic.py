from types import NoneType

import happyaml


def test_escape_double_quotes():
    assert happyaml._escape_quotes('"hello world"') == "hello world"


def test_escape_single_quotes():
    assert happyaml._escape_quotes("'goodbye cruel world'") == "goodbye cruel world"


def test_escape_escaped():
    assert happyaml._escape_quotes("'say \"hello\"'") == 'say "hello"'


def test_escape_dumb():
    assert happyaml._escape_quotes("already ecaped") == "already ecaped"


def test_escape_apostrophe():
    assert happyaml._escape_quotes("I'm here and you're there") == "I'm here and you're there"


def test_boolean_yes_value():
    assert type(happyaml._get_inline_value("bool: yes")) is bool


def test_boolean_true_value():
    assert type(happyaml._get_inline_value("bool: true")) is bool


def test_boolean_false_value():
    assert type(happyaml._get_inline_value("bool: false")) is bool


def test_none_null_value():
    assert type(happyaml._get_inline_value("none: null")) is NoneType


def test_none_tilda_value():
    assert type(happyaml._get_inline_value("none: ~")) is NoneType


def test_int_value():
    assert type(happyaml._get_inline_value("int: 1234")) is int


def test_float_value():
    assert type(happyaml._get_inline_value("duble: 3.14")) is float


def test_string_value():
    assert type(happyaml._get_inline_value("string: testing")) is str


def test_complex_key_value():
    assert type(happyaml._get_inline_value("':3 is my favorite emoji': true")) is bool


def test_list_value():
    assert type(happyaml._get_inline_value("- list item")) is str


def test_list_custom_type_value():
    assert type(happyaml._get_inline_value("- 1.41213")) is float


def test_simple_key():
    assert happyaml._get_inline_key("key: value") == "key"


def test_quoted_key():
    assert happyaml._get_inline_key("'language': '日本語'") == "language"


def test_complex_key():
    assert happyaml._get_inline_key("':3 is my favorite emoji': true") == ":3 is my favorite emoji"
