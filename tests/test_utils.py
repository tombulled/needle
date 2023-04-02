import pytest

from needle import utils

def test_prepare_arguments() -> None:
    def positional_only(arg: str, /):
        ...

    def positional_or_keyword(arg: str):
        ...

    def keyword_only(*, arg: str):
        ...

    def var_positional(*args: str):
        ...

    def var_keyword(**kwargs: str):
        ...

    def kitchen_sink(
        param_positional_only: str,
        /,
        param_positional_or_keyword: str,
        *param_var_positional: str,
        param_keyword_only: str,
        **param_var_keyword: str,
    ):
        ...

    assert utils.prepare_arguments(positional_only, {"arg": "foo"}) == (("foo",), {})
    assert utils.prepare_arguments(positional_or_keyword, {"arg": "foo"}) == (
        (),
        {"arg": "foo"},
    )
    assert utils.prepare_arguments(keyword_only, {"arg": "foo"}) == ((), {"arg": "foo"})
    assert utils.prepare_arguments(var_positional, {"args": ("foo", "bar", "baz")}) == (
        ("foo", "bar", "baz"),
        {},
    )
    assert utils.prepare_arguments(
        var_keyword, {"kwargs": {"name": "sam", "age": 43}}
    ) == ((), {"name": "sam", "age": 43})
    assert utils.prepare_arguments(
        kitchen_sink,
        {
            "param_positional_only": "param_positional_only",
            "param_positional_or_keyword": "param_positional_or_keyword",
            "param_var_positional": ("arg1", "arg2"),
            "param_keyword_only": "param_keyword_only",
            "param_var_keyword": {"key1": "val1", "key2": "val2"},
        },
    ) == (
        ("param_positional_only", "arg1", "arg2"),
        {
            "param_positional_or_keyword": "param_positional_or_keyword",
            "param_keyword_only": "param_keyword_only",
            "key1": "val1",
            "key2": "val2",
        },
    )

    with pytest.raises(ValueError):
        utils.prepare_arguments(positional_only, {})