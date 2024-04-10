from dataclasses import dataclass, field
from typing import Any

import pytest

from lenient_string_formatter import LenientFormatter


@dataclass
class FormatTestCase:
    name: str
    template: str
    expected: str | None = None
    args: tuple[Any, ...] = ()
    kwargs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.args and not self.kwargs and not self.expected:
            self.expected = self.template
        assert self.expected is not None


class HasAttr:
    def __init__(self, value: Any):
        self.attr = value


FORMAT_TEST_CASES = (
    FormatTestCase(name="no-fields", template="No fields", expected="No fields"),
    FormatTestCase(
        name="named-simple", template="{foo}", expected="bar", kwargs={"foo": "bar"}
    ),
    FormatTestCase(
        name="named-unmatched",
        template="{unknown}",
        expected="{unknown}",
        kwargs={"foo": "bar"},
    ),
    FormatTestCase(
        name="named-mixed",
        template="{name} {age}",
        expected="Alice {age}",
        kwargs={"name": "Alice"},
    ),
    FormatTestCase(
        name="named-format-spec",
        template="{a:2}{x:03}",
        expected="a {x:03}",
        kwargs={"a": "a"},
    ),
    FormatTestCase(name="named-attr", template="{obj.attr}"),
    FormatTestCase(name="named-item", template="{obj[key]}"),
    FormatTestCase(name="named-convert", template="{a} {b!r} {c!s} {d!a}"),
    FormatTestCase(
        name="numbered-simple", template="{0}", expected="bar", args=("bar",)
    ),
    FormatTestCase(name="numbered-unmatched", template="{0}"),
    FormatTestCase(
        name="numbered-mixed", template="{0} {1}", expected="Alice {1}", args=("Alice",)
    ),
    FormatTestCase(
        name="numbered-format-spec",
        template="{1:2}{0:03}",
        expected="{1:2}001",
        args=(1,),
    ),
    FormatTestCase(name="numbered-attr", template="{0.attr}"),
    FormatTestCase(name="numbered-item", template="{0[key]}"),
    FormatTestCase(name="numbered-convert", template="{0} {1!r} {2!s} {3!a}"),
    FormatTestCase(name="auto-and-numbered", template="{} {1} {} {0}"),
    FormatTestCase(name="auto-simple", template="{}", expected="bar", args=("bar",)),
    FormatTestCase(name="auto-unmatched", template="{}"),
    FormatTestCase(
        name="auto-mixed", template="{} {}", expected="Alice {}", args=("Alice",)
    ),
    FormatTestCase(
        name="auto-format-spec", template="{:2}{:03}", expected="a {:03}", args=("a",)
    ),
    FormatTestCase(
        name="auto-attr",
        template="{.attr}{.attr}",
        expected="a{.attr}",
        args=(HasAttr("a"),),
    ),
    FormatTestCase(
        name="auto-item",
        template="{[key]}{[0]}",
        expected="a{[0]}",
        args=(dict(key="a"),),
    ),
    FormatTestCase(name="auto-convert", template="{} {!r} {!s} {!a}"),
    FormatTestCase(
        name="recursive-simple", template="{:{}}", expected="a  ", args=("a", 3)
    ),
    FormatTestCase(name="recursive-unmatched", template="{:{}}"),
    FormatTestCase(
        name="recursive-mixed-1", template="{0:{1}}", expected="{0:{1}}", args=("a",)
    ),
    FormatTestCase(
        name="recursive-mixed-2", template="{1:{0}}", expected="{1:{0}}", args=("a",)
    ),
    FormatTestCase(name="convert-format-spec", template="{!r:2} {!s:03} {!a:4}"),
    FormatTestCase(
        name="named-repeats",
        template="{n}+{n}=2*{n}",
        expected="3+3=2*3",
        kwargs={"n": "3"},
    ),
    FormatTestCase(
        name="numbered-repeats",
        template="{0}+{0}=2*{0}",
        expected="3+3=2*3",
        args=("3",),
    ),
    FormatTestCase(
        name="auto-repeats",
        template="{}+{}=2*{}",
        expected="3+3=2*3",
        args=("3", "3", "3"),
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
