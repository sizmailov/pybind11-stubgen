class Bar(object):
    pass


class Foo(object):
    """Foo class docstring"""

    name: str
    count: int
    bar: Bar

    def f(self):  # type: (Foo) -> None
        ...

    @staticmethod
    def g():  # type: () -> None
        ...

    @property
    def str_prop(self):
        """
        :rtype: str
        """
        return "str"

    @property
    def int_prop(self):
        """
        :rtype: int
        """
        return 1

    @property
    def bar_prop(self):
        """
        :rtype: int
        """
        return self.bar
