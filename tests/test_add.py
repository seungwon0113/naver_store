from temp import add


def test_add() -> None:
    # given
    a, b = 1, 1
    # when
    result = add(a, b)
    # then
    assert result == 2
