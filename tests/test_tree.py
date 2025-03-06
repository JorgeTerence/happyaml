import backend


def test_empty():
    assert backend.build_tree([]) == []


def test_basic():
    doc = ["key: value"]
    assert backend.build_tree(doc) == doc


def test_nested():
    doc = [
        "branch:",
        "  leaf: 1",
    ]
    assert backend.build_tree(doc) == [(doc[0], [doc[1]])]


def test_multiple_leaves():
    doc = [
        "branch:",
        "  leaf: 1",
        "  apple: 2",
    ]
    assert backend.build_tree(doc) == [(doc[0], [doc[1], doc[2]])]


def test_multiple_branches():
    doc = [
        "apple_tree:",
        "  apple: 1",
        "  green_apple: 2",
        "orange_tree:",
        "  orange: 4",
    ]
    expected = [
        (doc[0], [doc[1], doc[2]]),
        (doc[3], [doc[4]]),
    ]
    assert backend.build_tree(doc) == expected


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
        (
            doc[0],
            [
                (
                    doc[1],
                    [
                        (
                            doc[2],
                            [
                                doc[3],
                                doc[4],
                                (doc[5], [doc[6]]),
                            ],
                        )
                    ],
                )
            ],
        )
    ]

    assert backend.build_tree(doc) == expected


def test_list():
    doc = [
        "- 1"
        "- 2"
        "- 3"
    ]
    assert backend.build_tree(doc) == doc


def test_list_of_obj():
    doc = [
        "level1:",
        "  - name: abc",
        "    code: 123",
    ]

    expected = [
        (doc[0], [doc[1], doc[2]])
    ]

    assert backend.build_tree(doc) == expected
