# https://docs.pytest.org/en/stable/how-to/assert.html

import pytest


def test_with_raises():
    with pytest.raises(ValueError) as exc_info:
        int("not_a_number")

    print(exc_info)
    # ValueError: invalid literal for int() with base 10: 'not_a_number'
    print(exc_info.value)
    # invalid literal for int() with base 10: 'not_a_number'
    print(str(exc_info.value))


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # テストを実行
# https://docs.pytest.org/en/stable/reference/reference.html#pytest-main
