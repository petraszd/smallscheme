from smallscheme.syntax import *
from smallscheme.runner import Environment

def test_evaluate():
    begin = Begin()
    begin.add_child(Number("1"))
    begin.add_child(Number("2"))

    assert 2 == begin.evaluate(Environment()).value

