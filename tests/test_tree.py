import happyaml2


def test_empty():
    assert happyaml2._build_tree([]) == []


def test_basic():
    doc = ["key: value"]
    assert happyaml2._build_tree(doc) == doc


def test_nested():
    doc = [
        "branch:",
        "  leaf: 1",
    ]
    assert happyaml2._build_tree(doc) == [{doc[0]: [doc[1]]}]


def test_multiple_leaves():
    doc = [
        "branch:",
        "  leaf: 1",
        "  apple: 2",
    ]
    assert happyaml2._build_tree(doc) == [{doc[0]: [doc[1], doc[2]]}]


def test_multiple_branches():
    doc = [
        "apple_tree:",
        "  apple: 1",
        "  green_apple: 2",
        "orange_tree:",
        "  orange: 4",
    ]
    expected = [
        {doc[0]: [doc[1], doc[2]]},
        {doc[3]: [doc[4]]},
    ]
    assert happyaml2._build_tree(doc) == expected


def test_deep_nesting():
    doc = [
        "level1:",
        "  level2:",
        "    level3:",
        "      step: 1",
        "      rest: 2",
        "      level4:",
        "        arrival: 1",
    ]

    expected = [
        {
            doc[0]: [
                {
                    doc[1]: [
                        {
                            doc[2]: [
                                doc[3],
                                doc[4],
                                {doc[5]: [doc[6]]},
                            ]
                        }
                    ]
                }
            ]
        }
    ]

    assert happyaml2._build_tree(doc) == expected
