from smallscheme import SchemeError
from smallscheme.syntax import *
from smallscheme.runner import *
import py

def test_evaluate():
    var = Variable("foo")
    env = Environment()
    with py.test.raises(SchemeError):
        var.evaluate(env)

    env.define(Variable("foo"), Number("123"))
    assert 123 == var.evaluate(env).value

