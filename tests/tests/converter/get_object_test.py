from typing import Optional, Union
from datetime import datetime, timezone

from attrs import define

from telebox.bot.type import Type
from telebox.bot.utils.converter import Converter


def test():
    @define(repr=False)
    class Foo(Type):
        created_at: datetime

    @define(repr=False)
    class Bar(Type):
        content: Union[int, str]

    @define(repr=False)
    class Baz(Type):
        foo: Foo
        foo_or_bar: Union[Foo, Bar]
        bars: list[Bar]
        message: Optional[str] = None
        created_at: Optional[datetime] = None

    converter = Converter()
    object_ = converter.get_object(
        data={
            "foo": {
                "created_at": 1753650020
            },
            "foo_or_bar": {
                "created_at": 1753650020
            },
            "bars": [
                {
                    "content": 12345
                },
                {
                    "content": "Message"
                }
            ],
            "message": "Text"
        },
        class_=Baz
    )
    expected_object = Baz(
        foo=Foo(
            created_at=datetime(
                year=2025,
                month=7,
                day=27,
                hour=21,
                minute=0,
                second=20,
                tzinfo=timezone.utc
            )
        ),
        foo_or_bar=Foo(
            created_at=datetime(
                year=2025,
                month=7,
                day=27,
                hour=21,
                minute=0,
                second=20,
                tzinfo=timezone.utc
            )
        ),
        bars=[
            Bar(
                content=12345
            ),
            Bar(
                content="Message"
            )
        ],
        message="Text"
    )

    assert object_ == expected_object


def test_unknown_field():
    @define(repr=False)
    class Foo:
        a: int
        b: str

    converter = Converter()
    object_ = converter.get_object(
        data={
            "a": 100,
            "b": "foobar",
            "c": "unknown"
        },
        class_=Foo
    )
    expected_object = Foo(
        a=100,
        b="foobar"
    )

    assert object_ == expected_object
