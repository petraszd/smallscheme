from smallscheme.runner import Environment
from smallscheme.syntax import *
from smallscheme.datatypes import *
from smallscheme import SchemeError
import py

def test_evaluate():
    cons = Cons()
    cons.add_child(Number("1"))
    # needs 2 not 1 arg
    with py.test.raises(SchemeError):
        cons.evaluate(Environment())

    cons.add_child(Number("2"))
    result = cons.evaluate(Environment())
    assert Pair == type(result)

    cons.add_child(Number("3"))
    # needs 2 not 3 args
    with py.test.raises(SchemeError):
        cons.evaluate(Environment())
