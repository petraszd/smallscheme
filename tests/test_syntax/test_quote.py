from smallscheme.runner import Environment
from smallscheme.syntax import *
from smallscheme.datatypes import *
from smallscheme import SchemeError

def test_evaluate():
    quote = Quote()
    quote.add_child(Number("1"))

    call = Call()
    call.add_child(Variable("foo"))

    quote.add_child(call)
    quote.add_child(Number("3"))

    result = quote.evaluate(Environment())

    assert 1 is result.car.value
    assert Symbol.table[Symbol.table.index("foo")] is result.cdr.car.car.value
    assert Null is result.cdr.car.cdr
    assert 3 is result.cdr.cdr.car.value
    assert Null is result.cdr.cdr.cdr

