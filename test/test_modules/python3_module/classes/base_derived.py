class Base(object):
    pass


class Derived(Base):
    pass


class DerivedDerived(Derived):
    pass


class Base2(object):
    pass


class Derived2(Base2):
    pass


class DerivedDerived2(Derived2):
    pass


class MultiDerived(DerivedDerived, DerivedDerived2):
    pass
