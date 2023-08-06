# pyguarantees

![License](https://img.shields.io/github/license/snimu/guarantees)
![PyPI Version](https://img.shields.io/pypi/v/pyguarantees)
![Tests](https://github.com/snimu/guarantees/actions/workflows/tests.yml/badge.svg)
![Coverage](coverage.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/pyguarantees)


This package has two components: 

- `test_guarantees`: guarantee unittest-coverage for functions and methods.
- `functional_guarantees`: guarantee types and other properties for parameters and return values of 
callables&mdash;functions and methods. 


# test_guarantees

"I will have to write a unittest for this function later", you say. This package ensures that you 
won't forget.

"Why does this function fail? I've tested it... omg I didn't even call it in my TestCase." Use this 
package to make sure that a function/method will be called or a class instance constructed 
in its respective `TestCase`.

Can be used for `unittest` and `pytest`.

## Example unittest

```python 
import unittest
from pyguarantees import test_guarantees as tg
from some_package import some_fct_with_test_guarantee


class ExampleClass:
  @tg.guarantee_test()  # tg.main will raise exception if there is not test for this method
  def foo(self):
    return self

  @classmethod  # works for classmethods
  @tg.guarantee_test()  # @tg.guarantee_usage possible in any of these methods, but optional
  def class_method(cls):
    return cls

  @staticmethod  # works for staticmethods
  @tg.guarantee_test()
  def static_method():
    return "static!"


@tg.guarantee_test()
@tg.guarantee_usage()  # make sure that this is called in all its tests
def add_one(a):
  return a + 1


@tg.guarantee_test()
@tg.guarantee_usage()  # Makes sure that __init__ is called in the test
class RegularClass:
  def __init__(self):
    self.x = 2


class ExampleTest(unittest.TestCase):
  @tg.implements_test_for(
    ExampleClass.foo,
    ExampleClass.class_method,
    ExampleClass.static_method
  )
  def test_foo(self):
    ExampleClass().foo()
    ExampleClass.class_method()
    ExampleClass.static_method()

  @tg.implements_test_for(add_one, some_fct_with_test_guarantee)
  def test_other(self):
    val = add_one(1)
    self.assertEqual(val, 2)

  @tg.implements_test_for(RegularClass)
  def test_regular_class(self):
    regular_class = RegularClass()
    ...


if __name__ == '__main__':
  tg.main()
```

As in the example, `pyguarantees.test_guarantees` will be abbreviated with `tg` from here on out.

Failing to use an [@tg.implements_test_for](#implements_test_for) for a function or method decorated with [@tg.guarantee_test](#guarantee_test)
leads to a [tg.exceptions.TestsNotImplementedError](#testsnotimplementederror), while failing to use this function or method in the 
corresponding test will lead to a [tg.exceptions.NotUsedInTestsError](#notusedintestserror) if it is decorated by 
[@tg.guarantee_usage](#guarantee_usage). These exceptions are only raised if the `unittest.TestCase` are called first 
and then checked by [tg.enforce](#enforce), or [tg.main](#main) is called to do both automatically.

Currently doesn't work with nested functions (defined inside of other callables). This might be fixed at some point.


## Example pytest

```python
# These imports are unused but necessary for pytest to find the tests that 
#  enforce the guarantees from tg
from pyguarantees.test_guarantees import \
  test_all_tests_implemented, test_functions_used_in_tests
from pyguarantees import test_guarantees as tg


@tg.guarantee_test()
def foo():
    return 1


@tg.guarantee_test()
@tg.guarantee_usage()
def bar():
    return 1


def test_foo():
    assert foo() == 1


def test_bar():
    assert bar() == 1
```

This is even simpler: just use [@tg.guarantee_test](#guaranteetest), [@tg.guarantee_usage](#guaranteeusage),
and [@tg.implements_test_for](#implementstestfor) as in [Example unittest](#example-unittest). No 
need to call [tg.main](#main) or [tg.enforce](#enforce).

**IMPORTANT**: If you use `pytest.mark.order` from the [pytest-order](https://pypi.org/project/pytest-order/)-package,
don't use `pytest.mark.order(-1)` or `pytest.mark.order(-2)` on your tests&mdash;it is important that 
[test_all_tests_implemented](#testalltestsimplemented) and [test_functions_used_in_tests](#testfunctionsusedintests) 
are used last by `pytest`.


## Decorators

The three decorators shown below have no effect without the [functions](#functions) 
of this package, specifically running [main](#main) or [enforce](#enforce) for `unittest`, 
and simply importing [test_all_tests_implemented](#testalltestsimplemented) and 
[test_functions_used_in_tests](#testfunctionsusedintests) into one of your test-files.


### guarantee_test

Takes no arguments.

Any function, method, or class (except, for the moment, ones nested inside of other callables) 
decorated with `@tg.guarantee_test`
that is in the scope of unittest will force unittest to throw an exception should 
it not be in an [@tg.implements_test_for](#implements_test_for).

Currently, it is necessary to include the brackets&mdash;`()`&mdash; so that 
the function is registered. This executes the decorator once but not the callable that 
it decorates, making it computationally inexpensive.

Having a function (or method) decorated like follows:

```python
@tg.guaranteed()
def foo():
  pass
```

but not having a test in your `unittest.TestCase` decorated by `@implements_test_for(foo)` 
would lead to a [TestsNotImplementedError](#testsnotimplementederror) being raised.

The same works for classes.


### guarantee_usage

Takes no arguments.

Must be used below [@tg.guarantee_test](#guarantee_test), otherwise it is ignored.

Just like with `@tg.guarantee_test`, brackets are not optional, but the execution of 
the decorator is computationally inexpensive.

A function decorated as follows:

```python 
@tg.guaranteed()
@tg.calls()
def foo():
  pass
```

with a unittest that looks something like this:

```python 
# for unittest:
class TestExample(unittest.TestCase):
  @tg.covers(foo)
  def test_foo(self):
    ...  # some code that doesn't call foo


# for pytest:
@tg.covers(foo)
def test_foo():
  ...  # some code that doesn't call foo
```

would lead to a [NotUsedInTestsError](#notusedintestserror) being raised. 

In this scenario, if `foo` is an argument in several 
[@tg.implements_test_for](#implements_test_for),
`@tg.guarantee_usage` makes certain that `foo` is used in every test-function 
decorated in such a way.

Special case: For classes, `@tg.guarantee_usage` guarantees that `__init__` is called.
For a callable class, this still holds; to guarantee that the `__call__`-method is called
in the test, it has to be decorated by `@tg.guarantee_usage` itself, not the class it belongs to. 


### implements_test_for

- `args`: Give any function or method that the corresponding test is meant for.
- `kwargs`: The value will be used like an `arg`, while the key will be ignored.

Functions and methods that weren't decorated by [@tg.guarantee_test](#guarantee_test) 
lead to a user-warning but are ignored otherwise.

Usage might look as follows:

```python 
# for unittest:
class TestExample(unittest.TestCase):
  @tg.covers(function1, function2, this_key_is_ignored=function3)
  def test_example(self):
    ...


# for pytest:
@tg.covers(function1, function2, this_key_is_ignored=function3)
def test_example():
  ...
```

## Functions

Four functions are provided by `pyguarantees.test_guarantees`, all directly under
`tg`. 

For `unittest`, at least one of [main](#main) or [enforce](#enforce) 
has to be used for the [decorators](#decorators)
to have an effect. 

For `pytest`, both [test_all_tests_implemented](#testalltestsimplemented) 
and [test_functions_used_in_tests](#testfunctionsusedintests) have to be imported 
into one of your test-files.

### enforce

Takes no arguments.

Run this after running all your unittests. This runs additional unittests that 
check which functions violated their guarantees and raise [exceptions](#exceptions) 
accordingly.

It is recommended to only use this function when using a complicated unittest-setup.
When using `unittest.main()`, it is recommended to use `tg.main()` instead.

### main

Takes no arguments.

Calls `unittest.main()` followed by [tg.enforce](#enforce).

### test_all_tests_implemented

Takes no arguments.

Import this into one of your files for [@tg.guarantee_test](#guaranteetest) and 
[@tg.implements_test_for](#implementstestfor) to have any effect.

### test_functions_used_in_tests

Takes no arguments.

Import this and [test_all_tests_implemented](#testalltestsimplemented) 
into one of your files for [@tg.guarantee_usage](#guaranteeusage) to 
have any effect.

## Exceptions

`Exceptions` are located under `tg.exceptions`.

There are two custom `Exceptions` as presented below.

### TestsNotImplementedError

Arguments of `tg.exceptions.TestsNotImplementedError`:

- `functions` (type `callable`): The callables that weren't mentioned in a 
[`@tg.implements_test_for`](#implements_test_for).

Members of `tg.exceptions.TestsNotImplementedError`:

- `functions` (type `callable`): The callables that weren't mentioned in a 
[`@tg.implements_test_for`](#implements_test_for).
- `description` (type `str`): The error string printed when the exception is raised
and not caught.

The output of raising this exception might look something like:

    <Traceback...>

    pyguarantees.test_guarantees.exceptions.TestsNotImplementedError: 

        No tests were implemented for the following methods and functions: 
    
        1. Missing test-case for the following callable: 
            Name: 		foo
            Module: 	__main__
        2. Missing test-case for the following callable: 
            Name: 		bar
            Module: 	__main__

### NotUsedInTestsError
Arguments of `tg.exceptions.NotUsedInTestsError`:

- `functions` (type: `callable`): The callables that were mentioned in a 
[`@tg.implements_test_for`](#implements_test_for) but not used in the corresponding
test.

Members of `tg.exceptions.NotUsedInTestsError`:

- `functions` (type: `callable`): The callables that were mentioned in a 
[`@tg.implements_test_for`](#implements_test_for) but not used in the corresponding
test.
- `description` (type: `str`): The error string printed when the exception is raised
and not caught.

A possible error message might look like the following:
    
    <Traceback...>

    pyguarantees.test_guarantees.exceptions.NotUsedInTestsError:

    The following objects were not used in their assigned tests: 

	1. The following callable was not called in its assigned tests: 
		Name: 		foo
		Module: 	__main__
		This callable is tested but not called in the following test-cases: 
					- Name: 	TestFoo.test_foo1
					   Module: 	__main__
					- Name: 	TestFoo.test_foo2
					   Module: 	__main__
	2. The following callable was not called in its assigned tests: 
		Name: 		bar
		Module: 	some_module
		This callable is tested but not called in the following test-cases: 
					- Name: 	TestBar.test_bar
					   Module: 	test_some_module


# functional_guarantees

Few things are more useful in programming than the ability to constrain a program's possible behaviors 
and communicate those constraints clearly in code. Statically typed languages do this with types, scope modifiers, 
and lifetime modifiers, among others (`int`, `static`, `private`, `const`, etc.). These are static constraints&mdash;or 
static guarantees&mdash;in that they are evaluated statically, before runtime.

Oftentimes, a program also has dynamic guarantees, evaluated during runtime&mdash;assertions, for example. 
A function dealing with division, for example, has to deal with the special case of division by zero. 

`pyguarantees.functional_guarantees`, abbreviated with `fg` from here on out, enables both types of guarantees to be 
defined in Python where they should happen: function (or method) signatures. This is where statically typed 
languages put their static guarantees (a typical function signature looks something like 
`scope-etc-modifiers return-type function-name(parameter-type parameter-name)`) and where in my opinion, dynamic 
guarantees belong as well.

This might have the following advantages:
- Make code more readable by having constraints in a predefined place.
- Make code easier to write by providing important information about APIs in a glancable way.
- Make it possible to include information on dynamic constraints in automatically generated documentation.
- Encourage programmers to think about these constraints while writing the functions&mdash;a type of 
test-driven development directly at the function (seeing parts of the "tests" in the function-signature
might assist readability of code, as well). 

This package is an attempt to open up at least some of these advantages to Python-users at least partially, 
given the constraints of the Python-language. 

## Example 1

This example shows basic usage of the `fg` package for parameters of functions.

```python
import numpy as np
from src.pyguarantees import functional_guarantees as fg

from your_module import your_custom_error_callback


# One of many built-in guarantees using one of many built-in options
@fg.constrain(parameters=[fg.IsInt("num", minimum=3)])
def add_one(num):
  return num + 1


# Use fg.IsClass to guarantee all types and classes that don't have specific guarantees 
#  in fg. If they do, it is recommended to use those specific guarantees.
@fg.constrain(
  parameters=[
    fg.IsClass(
      "X",
      class_type=np.ndarray,
      dynamic_checks=[
        fg.DynamicCheck(check=lambda x: x.min() > 0, description="min: 0"),
        fg.DynamicCheck(check=lambda x: x.var() < 5, description="var < 5"),
        fg.DynamicCheck(check=lambda x: x.shape == (3, 80, 80), description="shape (3, 80, 80")
      ],
      error_callback=your_custom_error_callback
    ),
    fg.IsClass("mean", class_type=np.ndarray),
    fg.IsClass("std", class_type=np.ndarray)
  ],
  returns=fg.IsClass("", class_type=np.ndarray)
)
def normalize(X, mean, std):
  return (X - mean) / std
```


## Example 2

This example shows the use of the `fg`-package for testing.

```python 
import unittest
from pyguarantees import functional_guarantees as fg


@fg.constrain(returns=fg.IsInt("a"))
def foo(a):
  return a


@fg.constrain(returns=fg.IsInt("a"))
def bar(a):
  return a


class TestExample(unittest.TestCase):
  def test_example(self):
    # chain functions and automatically raise exceptions if at any point
    #   the guarantees for parameters and/or return values aren't fulfilled.
    foo(bar(1))   
```


## add_guarantees

Add [guarantees](#guarantees) to a callable. 

**Arguments**:
- **param_guarantees** A list of [Guarantees](#guarantee) that will work on the parameters of the callable 
decorated by `add_guarantees`. Must fulfill the following properties:
  - Be in the order that the arguments are defined in the callable-signature. If you have for example
    a function `def foo(a, b)`, where `a` should be an `int` and `b` a `str`, `param_guarantees` has to 
    be something like `[fg.IsInt("a"), fg.IsStr("b")`.
  - 
- **return_guarantee** A single [Guarantee](#guarantee) on the return values. 
- **is_staticmethod** Needed to deal with `staticmethods` (`classmethod` and regular methods work automatically).

## Guarantees

There are several pre-defined guarantees. Most are based on the [TypeGuarantee](#typeguarantee).

### Guarantee

The base class of all guarantees in `fg`.

### TypeGuarantee





> this README is currently under development. More is coming.