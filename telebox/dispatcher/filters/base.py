from abc import ABC, abstractmethod
from enum import Enum


class AbstractFilter(ABC):

    def __invert__(self):
        return FilterExpression(self).__invert__()

    def __and__(self, other):
        return FilterExpression(self).__and__(other)

    def __or__(self, other):
        return FilterExpression(self).__or__(other)

    @abstractmethod
    def get_value(self, *args, **kwargs):
        pass

    @abstractmethod
    def check_value(self, value) -> bool:
        pass


class ExpressionType(Enum):
    NONE = "none"
    FILTER = "filter"
    INVERT = "invert"
    AND = "and"
    OR = "or"


class AbstractExpression(ABC):

    def __invert__(self):
        return InvertExpression(self)

    def __and__(self, other):
        if isinstance(other, AndExpression):
            return AndExpression(self, *other)
        elif isinstance(other, AbstractExpression):
            return AndExpression(self, other)
        elif isinstance(other, AbstractFilter):
            return AndExpression(self, FilterExpression(other))

        return NotImplemented

    def __or__(self, other):
        if isinstance(other, OrExpression):
            return OrExpression(self, *other)
        elif isinstance(other, AbstractExpression):
            return OrExpression(self, other)
        elif isinstance(other, AbstractFilter):
            return OrExpression(self, FilterExpression(other))

        return NotImplemented

    @abstractmethod
    def get_type(self) -> ExpressionType:
        pass


class NoneExpression(AbstractExpression):

    def __invert__(self):
        return NotImplemented

    def __and__(self, other):
        return NotImplemented

    def __or__(self, other):
        return NotImplemented

    def get_type(self) -> ExpressionType:
        return ExpressionType.NONE


class AbstractSingleExpression(AbstractExpression, ABC):

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"{type(self).__name__}({self.value!r})"


class AbstractMultipleExpression(AbstractExpression, ABC):

    def __init__(self, *values):
        self.values = values

    def __repr__(self):
        return f"{type(self).__name__}({', '.join(repr(i) for i in self.values)})"

    def __iter__(self):
        return iter(self.values)


class FilterExpression(AbstractSingleExpression):

    def get_type(self) -> ExpressionType:
        return ExpressionType.FILTER


class InvertExpression(AbstractSingleExpression):

    def __invert__(self):
        return self.value

    def get_type(self) -> ExpressionType:
        return ExpressionType.INVERT


class AndExpression(AbstractMultipleExpression):

    def __and__(self, other):
        if isinstance(other, AndExpression):
            return AndExpression(*self, *other)
        elif isinstance(other, AbstractSingleExpression):
            return AndExpression(*self, other)

        return super().__and__(other)

    def get_type(self) -> ExpressionType:
        return ExpressionType.AND


class OrExpression(AbstractMultipleExpression):

    def __or__(self, other):
        if isinstance(other, OrExpression):
            return OrExpression(*self, *other)
        elif isinstance(other, AbstractSingleExpression):
            return OrExpression(*self, other)

        return super().__or__(other)

    def get_type(self) -> ExpressionType:
        return ExpressionType.OR
