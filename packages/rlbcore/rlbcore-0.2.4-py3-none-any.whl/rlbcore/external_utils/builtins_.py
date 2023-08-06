import functools
import typing as t
from pprint import pformat

from omegaconf import MISSING, DictConfig, ListConfig, MissingMandatoryValue, OmegaConf


def nested_dict_contains_dot_key(
    dictionary: dict[str, t.Any] | DictConfig, dot_key: str
) -> bool:
    """Return True if the dictionary contains dot_key in the exact nested position.

    Args:
        dictionary: The dictionary to check.
        dot_key: The dot key to check. For example, "a.b.c" will check if the dictionary
            at the key "a" contains a dict as value for the key "b" which contains the
            key "c".

    Returns:
        True only if the dictionary contains the dot key in the exact nested position

    NOTE:
        This function is currently used in `rlbcore.cli.run` to check if the config
        overrides provided through the CLI are keys in the config.

    Example:
        ```python
        >>> assert nested_dict_contains_dot_key(dict(a=0, b=dict(c=0, d=0)), "b.d")
        >>> assert not nested_dict_contains_dot_key(dict(a=0, b=dict(c=0, d=0)), "d")

        ```
    """
    if "." not in dot_key:
        return dot_key in dictionary
    key_to_check, _, rem_dot_key = dot_key.partition(".")
    if key_to_check in dictionary:
        return nested_dict_contains_dot_key(dictionary[key_to_check], rem_dot_key)
    else:
        return False


def update_maybe_nested(
    config: dict[str, t.Any] | DictConfig, key: str, value: t.Any
) -> None:
    """Set value of possibly nested `key` in config.

    Args:
        config: Dictionary with arbitrary level of nesting.
        key: Uses dot notation if nested.
        value: Value to set for key.

    Returns:
        None, but updates config in place.

    Example:
        ```python
        >>> config = dict(
        ...    a=0,
        ...    b=dict(
        ...        c="???",
        ...        d=dict(
        ...            e=0,
        ...            f="???",
        ...        ),
        ...    ),
        ... )
        >>> update_maybe_nested(
        ...    config,
        ...    "b.d.f",
        ...    1
        ... )
        >>> config
        {'a': 0, 'b': {'c': '???', 'd': {'e': 0, 'f': 1}}}

        ```
    """
    if "." not in key:
        config[key] = value
        return
    else:
        key, _, sub_key = key.partition(".")
        update_maybe_nested(config[key], sub_key, value)


def get_top_level_key(
    config: dict[str, t.Any] | DictConfig | list[t.Any] | ListConfig, key: str
) -> t.Any:
    """Return value of top level `key` in config.

    Args:
        config: The config to get the key from.
        key: The key to get.

    Returns:
        The value of the key.

    Example: Get top level key from dict
        ```python
        >>> import pytest
        >>> get_top_level_key(dict(a=0, b=1), "a")
        0
        >>> get_top_level_key(dict(a=0, b=1), "b")
        1
        >>> with pytest.raises(KeyError):
        ...     get_top_level_key(dict(a=0, b=1), "c")

        ```
    Example: Get top level key from list
        ```python
        >>> get_top_level_key([0, 1], "[0]")
        0
        >>> get_top_level_key([0, 1], "[1]")
        1

        ```
    Example: Get top level key from DictConfig
        ```python
        >>> import pytest
        >>> from omegaconf import OmegaConf
        >>> config = OmegaConf.create(dict(a=0, b=1))
        >>> get_top_level_key(config, "a")
        0
        >>> get_top_level_key(config, "b")
        1
        >>> with pytest.raises(KeyError):
        ...     get_top_level_key(config, "c")

        ```
    Example: Get top level key from ListConfig
        ```python
        >>> from omegaconf import OmegaConf
        >>> config = OmegaConf.create([0, 1])
        >>> get_top_level_key(config, "[0]")
        0
        >>> get_top_level_key(config, "[1]")
        1

        ```
    """
    if isinstance(config, (DictConfig, dict)):
        return config[key]
    assert key.startswith("[") and key.endswith("]"), key
    assert "][" not in key, f"Not top level key: {key}"
    return config[int(key[1:-1])]


def select_maybe_nested(
    config: dict[str, t.Any] | DictConfig | list[t.Any] | ListConfig, key: str
) -> t.Any:
    """Return value of possibly nested `key` in config.

    Args:
        config: Dictionary with arbitrary level of nesting.
        key: Uses dot notation if nested.

    Returns:
        None, but updates the config in place.

    Example: Select nested key from dict
        ```python
        >>> select_maybe_nested(
        ...    dict(
        ...        a=0,
        ...        b=dict(
        ...            c="???",
        ...            d=dict(
        ...                e=0,
        ...                f="???",
        ...            ),
        ...        ),
        ...    ),
        ...    "b.d"
        ... )
        {'e': 0, 'f': '???'}

        ```
    Example: Select nested key from list
        ```python
        >>> select_maybe_nested(
        ...    [
        ...        0,
        ...        [
        ...            "???",
        ...            [
        ...                0,
        ...                "???",
        ...            ],
        ...        ],
        ...    ],
        ...    "[1][1]"
        ... )
        [0, '???']

        ```
    """
    if ("." not in key and "][" not in key) or key in config:
        try:
            return get_top_level_key(config, key)
        except (KeyError, IndexError) as e:
            raise KeyError(f"Key {key} not found in config") from e
    if "][" in key and "." in key:
        is_list = key.index("][") < key.index(".")
        if is_list:
            top_key, _, sub_key = key.partition("][")
            top_key = f"{top_key}]"
            sub_key = f"[{sub_key}"
        else:
            top_key, _, sub_key = key.partition(".")
    elif "][" in key:
        top_key, _, sub_key = key.partition("][")
        top_key = f"{top_key}]"
        sub_key = f"[{sub_key}"
    else:
        top_key, _, sub_key = key.partition(".")
    try:
        return select_maybe_nested(get_top_level_key(config, top_key), sub_key)
    except (KeyError, IndexError) as e:
        raise KeyError(f"Key {key} not found in config") from e


@functools.singledispatch
def get_missing_keys(config: dict[str, t.Any] | DictConfig) -> list[str]:
    """Return list of keys with value = "???" in config in dot key format.

    Missing keys may be arbitrarily nested. For nested keys with missing values, the
    keys are returned in dot format such that the key can be accessed with OmegaConf as
    `OmegaConf.select(missing_key)`

    Args:
        config: Dictionary with arbitrary level of nesting.

    Example: Get missing keys from DictConfig
        ```python
        >>> get_missing_keys(
        ...    DictConfig(
        ...         dict(
        ...             a=0,
        ...             b=0,
        ...             c="???",
        ...             d=dict(
        ...                 e=0,
        ...                 f="???",
        ...             ),
        ...         )
        ...     )
        ... )
        ['c', 'd.f']

        ```

    Example: Get missing keys from dict
        ```python
        >>> get_missing_keys(
        ...    dict(
        ...        a=0,
        ...        b=0,
        ...        c="???",
        ...        d=dict(
        ...            e=0,
        ...            f="???",
        ...        ),
        ...    )
        ... )
        ['c', 'd.f']

        ```
    """
    raise NotImplementedError(f"for config of type {type(config)}")


@get_missing_keys.register
def _get_missing_keys_dict_config(config: DictConfig) -> list[str]:
    # sourcery skip: remove-redundant-pass
    result: list[str] = []
    to_check: list[str] = []
    for key in config:
        assert isinstance(key, str)
        if OmegaConf.is_missing(config, key):
            result.append(key)
        elif isinstance(config[key], (DictConfig, dict)):
            to_check.append(key)
        else:
            # Key is present. We're not interested in it.
            pass
    for key in to_check:
        missing_keys = _get_missing_keys_dict_config(config[key])
        missing_dot_keys = (f"{key}.{x}" for x in missing_keys)
        result.extend(missing_dot_keys)
    return result


@get_missing_keys.register
def _get_missing_keys_dict(config: dict) -> list[str]:  # type: ignore
    result: list[str] = []
    to_check: list[str] = []
    for key, value in config.items():  # type: ignore
        if value == MISSING:
            result.append(key)  # type: ignore
        elif isinstance(value, dict):
            to_check.append(key)  # type: ignore
    for key in to_check:
        missing_keys = _get_missing_keys_dict(config[key])
        missing_dot_keys = (f"{key}.{x}" for x in missing_keys)
        result.extend(missing_dot_keys)
    return result


def recursive_iter(
    config: DictConfig | dict[str, t.Any] | ListConfig | list[t.Any],
    list_is_leaf: bool = True,
    base_key: str = "",
) -> t.Iterator[str]:
    """Iterate over all keys in config, including keys in nested configs.

    Args:
        config: config to iterate over
        list_is_leaf: if True, will not iterate over list and ListConfig values
        base_key: base key to prepend to all keys

    Yields:
        key in config

    Raises:
        MissingMandatoryValue: if config contains missing keys, i.e. if
            `len(get_missing_keys(config)) > 0`

    Example: Iterate over DictConfig
        ```python
        >>> list(
        ...     recursive_iter(
        ...         DictConfig(
        ...             dict(
        ...                 a=0,
        ...                 b=dict(
        ...                     c=0,
        ...                     d=dict(e=0),
        ...                     f=dict(g=0),
        ...                     h=0,
        ...                 )
        ...             )
        ...         )
        ...     )
        ... )
        ['a', 'b', 'b.c', 'b.d', 'b.d.e', 'b.f', 'b.f.g', 'b.h']
        >>> import pytest
        ... with pytest.raises(MissingMandatoryValue):
        ...     list(recursive_iter(DictConfig(dict(a=0, b=dict(c=0, d="???")))))

        ```

    Example: Iterate over dict
        ```python
        >>> list(
        ...     recursive_iter(
        ...         dict(
        ...             a=0,
        ...             b=dict(
        ...                 c=0,
        ...                 d=dict(e=0),
        ...                 f=dict(g=0),
        ...                 h=0,
        ...             )
        ...         )
        ...     )
        ... )
        ['a', 'b', 'b.c', 'b.d', 'b.d.e', 'b.f', 'b.f.g', 'b.h']

        ```

    Example: Iterate over dict with list
        ```python
        >>> list(
        ...     recursive_iter(
        ...         dict(
        ...             a=0,
        ...             b=dict(c=[1, 2, 3])
        ...         ),
        ...     )
        ... )
        ['a', 'b', 'b.c']

        ```

    Example: Iterate over dict with list and list_is_leaf=False
        ```python
        >>> list(
        ...     recursive_iter(
        ...         dict(
        ...             a=0,
        ...             b=dict(c=[1, 2, 3])
        ...         ),
        ...         list_is_leaf=False,
        ...     )
        ... )
        ['a', 'b', 'b.c', 'b.c.[0]', 'b.c.[1]', 'b.c.[2]']

        ```
    """
    yield from filter(None, _recursive_iter(config, list_is_leaf, base_key))


def _recursive_iter(
    config: t.Any, list_is_leaf: bool = True, base_key: str = ""
) -> t.Iterator[str | None]:
    if isinstance(config, (DictConfig, dict)):
        key_iter = iter(config)
    elif not list_is_leaf and isinstance(config, (ListConfig, list)):
        key_iter = range(len(config))
    else:
        return
    separator = "." if base_key else ""
    for key in key_iter:
        suffix = f"[{key}]" if isinstance(key, int) else key
        new_key = f"{base_key}{separator}{suffix}"
        try:
            value = config[key]  # type: ignore
        except MissingMandatoryValue as e:
            raise MissingMandatoryValue(
                f"Cannot iterate over config with missing keys: \n{pformat(config)}"
            ) from e
        if isinstance(value, type(MISSING)) and value == MISSING:
            raise MissingMandatoryValue(
                f"Cannot iterate over config with missing keys: \n{pformat(config)}"
            )
        yield new_key
        yield from recursive_iter(value, list_is_leaf, new_key)


def iter_leaves(
    config: DictConfig | dict[str, t.Any] | ListConfig | list[t.Any],
    list_is_leaf: bool = True,
) -> t.Iterator[str]:
    """Return an iterator over keys whose values are not DictConfigs.

    Args:
        config: config to iterate over
        list_is_leaf: if True, any key containing a list of values will be treated as
            a leaf node

    Returns:
        iterator over keys whose values are not DictConfigs or dicts (or lists
            and ListConfigs if list_is_leaf is False)

    Example: Iterate over DictConfig
        ```python
        >>> list(
        ...     iter_leaves(
        ...         DictConfig(
        ...             dict(
        ...                 a=0,
        ...                 b=dict(
        ...                     c=0,
        ...                     d=dict(e=0),
        ...                     f=dict(g=0),
        ...                     h=0,
        ...                 )
        ...             )
        ...         )
        ...     )
        ... )
        ['a', 'b.c', 'b.d.e', 'b.f.g', 'b.h']

        ```

    Example: Iterate over dict
        ```python
        >>> list(
        ...     iter_leaves(
        ...         dict(
        ...             a=0,
        ...             b=dict(
        ...                 c=0,
        ...                 d=dict(e=0),
        ...                 f=dict(g=0),
        ...                 h=0,
        ...             )
        ...         )
        ...     )
        ... )
        ['a', 'b.c', 'b.d.e', 'b.f.g', 'b.h']

        ```

    Example: if missing values ("???") are present, an exception is raised
        ```python
        >>> import pytest
        ... with pytest.raises(MissingMandatoryValue):
        ...     list(iter_leaves(DictConfig(dict(a=0, b=dict(c=0, d="???")))))

        ```

    Example: list or ListConfig is treated as a leaf node
        ```python
        >>> list(
        ...    iter_leaves(
        ...        dict(
        ...            a=0,
        ...            b=dict(c=0),
        ...            d=dict(e=[0, 1, 2]),
        ...        ),
        ...        list_is_leaf=True,
        ...    )
        ... )
        ['a', 'b.c', 'd.e']

        ```

    Example: list or ListConfig is NOT treated as a leaf node
        ```python
        >>> list(
        ...    iter_leaves(
        ...        dict(
        ...            a=0,
        ...            b=dict(c=0),
        ...            d=dict(e=[0, 1, 2]),
        ...        ),
        ...        list_is_leaf=False,
        ...    )
        ... )
        ['a', 'b.c', 'd.e.[0]', 'd.e.[1]', 'd.e.[2]']

        ```
    """
    for key in recursive_iter(config, list_is_leaf):
        if _is_leaf_type(select_maybe_nested(config, key), list_is_leaf):
            yield key


def _is_leaf_type(value: t.Any, list_is_leaf: bool) -> bool:
    non_leaf_types = t.cast(tuple[type[t.Any], ...], (DictConfig, dict))
    if not list_is_leaf:
        non_leaf_types = non_leaf_types + (ListConfig, list)
    return not isinstance(value, non_leaf_types)


def iter_leaf_items(
    config: DictConfig | dict[str, t.Any] | ListConfig | list[t.Any],
    list_is_leaf: bool = True,
) -> t.Iterator[tuple[str, t.Any]]:
    """Iterate recursively over all key, value pairs (even nested) in config.

    Args:
        config: The config to iterate over.
        list_is_leaf: If True, any key containing a list of values will be treated as
            a leaf node

    Returns:
        An iterator over key, (leaf) value pairs.

    Raises:
        MissingMandatoryValue, if config contains missing keys, i.e. if
        `len(get_missing_keys(config)) > 0`

    Example: Iterate over all leaf items in a DictConfig
        ```python
        >>> list(
        ...     iter_leaf_items(
        ...         DictConfig(
        ...             dict(
        ...                 a=0,
        ...                 b=dict(
        ...                     c=1,
        ...                     d=dict(e=2),
        ...                     f=dict(g=3),
        ...                     h=4,
        ...                 )
        ...             )
        ...         )
        ...     )
        ... )
        [('a', 0), ('b.c', 1), ('b.d.e', 2), ('b.f.g', 3), ('b.h', 4)]

        ```

    Example: Iterate over all leaf items in a dict
        ```python
        >>> list(
        ...     iter_leaf_items(
        ...         dict(
        ...             a=0,
        ...             b=dict(
        ...                 c=1,
        ...                 d=dict(e=2),
        ...                 f=dict(g=3),
        ...                 h=4,
        ...             )
        ...         )
        ...     )
        ... )
        [('a', 0), ('b.c', 1), ('b.d.e', 2), ('b.f.g', 3), ('b.h', 4)]

        ```

    Example: If some values are missing ("???"), an exception is raised
        ```python
        >>> import pytest
        ... with pytest.raises(MissingMandatoryValue):
        ...     list(iter_leaf_items(DictConfig(dict(a=0, b=dict(c=0, d="???")))))

        ```
    """
    for key in iter_leaves(config, list_is_leaf):
        yield key, select_maybe_nested(config, key)


def iter_leaf_values(
    config: DictConfig | dict[str, t.Any] | ListConfig | list[t.Any],
    list_is_leaf: bool = True,
) -> t.Iterator[t.Any]:
    """Iterate over all values in config, including keys in nested configs.

    Args:
        config: The config to iterate over.
        list_is_leaf: If True, any key containing a list of values will be treated as
            a leaf node

    Returns:
        An iterator over all (leaf) values in config.

    Raises:
        MissingMandatoryValue, if config contains missing keys, i.e. if
        `len(get_missing_keys(config)) > 0`

    Example: Iterate over all leaf values in a DictConfig
        ```python
        >>> list(
        ...     iter_leaf_values(
        ...         DictConfig(
        ...             dict(
        ...                 a=0,
        ...                 b=dict(
        ...                     c=1,
        ...                     d=dict(e=2),
        ...                     f=dict(g=3),
        ...                     h=4,
        ...                 )
        ...             )
        ...         )
        ...     )
        ... )
        [0, 1, 2, 3, 4]

        ```

    Example: If some values are missing ("???"), an exception is raised
        ```python
        >>> import pytest
        ... with pytest.raises(MissingMandatoryValue):
        ...     list(recursive_iter(DictConfig(dict(a=0, b=dict(c=0, d="???")))))

        ```
    """
    for key in iter_leaves(config, list_is_leaf):
        yield select_maybe_nested(config, key)
