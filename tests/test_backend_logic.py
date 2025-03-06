import backend


def test_root_indentation():
    assert backend._get_indentation("a: 1") == 0


def test_basic_indentation():
    assert backend._get_indentation("  nested: 1") == 2


def test_root_branch_bounds():
    doc = [
        "root:",
        "  branch: 1",
        "brother:",
        "  branch: 1",
    ]
    assert backend._get_branch_limit(doc, 0, 0) == 2
    assert backend._get_branch_limit(doc, 2, 0) == 4


def test_sibiling_bounds():
    doc = [
        "sibiling: 1",
        "root:",
        "  leaf1: 1",
        "  leaf2: 2",
        "  leaf3: 3",
        "  leaf4: 4",
    ]
    assert backend._get_branch_limit(doc, 1, 0) == 6


def test_deep_bounds():
    doc = [
        "level1:",
        "  level2:",
        "    level3:",
        "      step: 1",
        "      rest: 2",
        "      level4:",
        "        arrival: 1",
        "    sublevel: 3",
        "  sublevel: 2",
    ]
    assert backend._get_branch_limit(doc, 0, 0) == 9
    assert backend._get_branch_limit(doc, 1, 2) == 8
    assert backend._get_branch_limit(doc, 2, 4) == 7
    assert backend._get_branch_limit(doc, 5, 6) == 7


def test_inline_simple():
    assert backend._is_inline("number: 1")


def test_inline_nested():
    assert not backend._is_inline("branch:")


def test_inline_quoted():
    assert backend._is_inline("'quoted string': 'hello'")


def test_inline_arbitrary():
    assert backend._is_inline("bad spec design: true")


def test_inline_tricky():
    assert backend._is_inline("':': 'double-colon'")
