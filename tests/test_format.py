from dataclasses import dataclass, field
from typing import Any

import pytest

from lenient_string_formatter import LenientFormatter


@dataclass
class FormatTestCase:
    name: str
    template: str
    expected: str
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)


FORMAT_TEST_CASES = (
    FormatTestCase(name="no-fields", template="No fields", expected="No fields"),
    FormatTestCase(
        name="kwargs-simple", template="{foo}", expected="bar", kwargs={"foo": "bar"}
    ),
    FormatTestCase(
        name="kwargs-unmatched",
        template="{unknown}",
        expected="{unknown}",
        kwargs={"foo": "bar"},
    ),
    FormatTestCase(
        name="kwargs-mixed",
        template="{name} {age}",
        expected="Alice {age}",
        kwargs={"name": "Alice"},
    ),
    FormatTestCase(
        name="kwargs-format-spec",
        template="{name:10} {age:03}",
        expected="Alice     {age:03}",
        kwargs={"name": "Alice"},
    ),
    FormatTestCase(name="args-simple", template="{0}", expected="bar", args=("bar",)),
    FormatTestCase(name="args-unmatched", template="{0}", expected="{0}"),
    FormatTestCase(
        name="args-mixed", template="{0} {1}", expected="Alice {1}", args=("Alice",)
    ),
    FormatTestCase(
        name="args-format-spec",
        template="{0:10} {1:03}",
        expected="Alice     {1:03}",
        args=("Alice",),
    ),
)


@pytest.fixture
def formatter() -> LenientFormatter:
    return LenientFormatter()


@pytest.fixture(params=FORMAT_TEST_CASES, ids=lambda tc: tc.name)
def format_test_case(request: pytest.FixtureRequest) -> FormatTestCase:
    return request.param


def test_format(formatter: LenientFormatter, format_test_case: FormatTestCase):
    actual = formatter.format(
        format_test_case.template, *format_test_case.args, **format_test_case.kwargs
    )
    assert actual == format_test_case.expected
