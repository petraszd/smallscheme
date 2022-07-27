from smallscheme import SchemeError
from smallscheme.syntax import *
from smallscheme.runner import Environment
import py

def test_evaluate():
    node = Node()
    with py.test.raises(SchemeError):
        node.evaluate(Environment())
    node.add_child(Number("123"))
    assert 123 == node.evaluate(Environment()).value

