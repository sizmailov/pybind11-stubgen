def arg_mix(
    a: int,
    b: float = 0.5,
    /,
    c: str = "",
    *args: int,
    x: int = 1,
    y=int,
    **kwargs: dict[int, str],
):
    """Mix of positional, kw and variadic args

    Note:
        The `inspect.getfullargspec` does not reflect presence
        of pos-only args separator (/)
    """
    ...
