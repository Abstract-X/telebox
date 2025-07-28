import pytest
from attrs import define

from telebox.bot.utils.converter import Converter
from telebox.bot.type import Type
import telebox.bot.types


def test_types():
    converter = Converter()

    for name in telebox.bot.types.__all__:
        class_ = getattr(telebox.bot.types, name)

        if converter.check_class(class_):
            converter.check_class_fields(class_)


def test_invalid_type():
    @define(repr=False)
    class Foo(Type):
        a: ...

    converter = Converter()

    with pytest.raises(ValueError):
        converter.check_class_fields(Foo)
