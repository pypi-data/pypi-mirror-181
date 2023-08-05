def above_classmethod(fct):
    print(fct.__func__)
    return fct


def below_classmethod(fct):
    print(fct)
    return fct


class ExampleClass:
    @above_classmethod
    @classmethod
    @below_classmethod
    def foo(cls):
        return cls.__qualname__


if __name__ == '__main__':
    ec = ExampleClass()
    print(ec.foo.__func__)
    print(ec.foo)

"""
-----------------
above classmethod
-----------------

guarantee_test / guarantee_usage:
    if isinstance(fct, classmethod):
        add fct.__func__ instead of fct
        
implements_test_for:
    if fct not in fdata.keys() and fct is not fct.__func__:
        add fct to fdata and functions, remove fct.__func__
        

-----------------
below classmethod
-----------------

guarantee_test / guarantee_usage:
    add fct to fdata
    
implements_test_for:
    as above
        
"""
