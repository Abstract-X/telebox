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
    data = converter.get_data(
        Baz(
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
    )
    expected_data = {
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
    }

    assert data == expected_data
