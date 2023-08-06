import typing as t
from unittest.mock import MagicMock

AnyT = t.TypeVar("AnyT")


def null_object(
    cls: type[AnyT],
    property_returns: dict[str, t.Any] | None = None,
    method_returns: dict[str, t.Any] | None = None,
) -> AnyT:
    """Create a null object following the Null object pattern.

    Args:
        cls: The class of the object for which a null object will be created.
        property_returns: A dictionary mapping property names to the values that
            should be returned when the property is accessed.
        method_returns: A dictionary mapping method names to the values that should
            be returned when the method is called.

    Returns:
        A dummy object having the same spec as `cls` that does nothing for any method
        call.

    Example:
        ```python
        >>> import pytest
        ... class Foo:
        ...     def __init__(self, x: int):
        ...         self.x = x
        ...     def bar(self, y: list[int]) -> None:
        ...         y.append(self.x)
        ... actual_foo = Foo(1)
        ... l = []
        ... actual_foo.bar(l)
        ... assert l == [1]
        ... null_foo = null_object(Foo)
        ... new_l = []
        ... null_foo.bar(new_l)
        ... assert new_l == []
        ... with pytest.raises(AttributeError):
        ...     null_foo.x
        ... with pytest.raises(AttributeError):
        ...     null_foo.a_method_that_does_not_exist()

        ```

    Usage:
    ------
    Instead of the following pattern:
    ```python
    >>> foo: Foo | None = None
    ... if foo is not None:
    ...     foo.bar([])

    ```

    Do:
    ```python
    >>> foo = null_object(Foo)
    ... foo.bar([])  # This will do nothing

    ```
    """
    _property_returns = property_returns or {}
    _method_returns = method_returns or {}

    class NullObject(cls):  # type: ignore
        def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
            pass

        def __getattribute__(self, __name: str) -> t.Any:
            if __name in _property_returns:
                return _property_returns[__name]
            if __name in _method_returns:
                return MagicMock(return_value=_method_returns[__name])
            if hasattr(super(), __name):
                # If the attribute exists in the parent class, but attribute was not
                # specified in method or property returns, return it's mocked version
                return MagicMock()
            return super().__getattribute__(__name)  # type: ignore

    NullObject.__name__ = cls.__name__
    return t.cast(AnyT, NullObject())
