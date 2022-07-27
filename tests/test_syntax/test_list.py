from smallscheme.runner import Environment
from smallscheme.syntax import *
from smallscheme.datatypes import *
from smallscheme import SchemeError

def test_evaluate_empty():
    list_ = List()
    assert Null is list_.evaluate(Environment())

def test_evaluate_with_elems():
    list_ = List()
    list_.add_child(Number("1"))
    list_.add_child(Number("2"))

    result = list_.evaluate(Environment())
    assert Pair == type(result)
    assert 1 == result.car.value
    assert Pair == type(result.cdr)
    assert 2 == result.cdr.car.value
    assert Null is result.cdr.cdr

