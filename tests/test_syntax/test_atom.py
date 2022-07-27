from smallscheme.runner import Environment
from smallscheme.syntax import Atom

def test_evaluate():
    num = Atom("foo")
    assert num is num.evaluate(Environment())

def test_str():
    atom = Atom("foo")
    assert "foo" == str(atom)

