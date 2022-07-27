from smallscheme import SchemeError
from smallscheme.datatypes import Null
from smallscheme.syntax import *
from smallscheme.runner import *
import py

def test_evaluate():
    define = Define()
    define.add_child(Variable("a"))
    define.add_child(Number("123"))

    env = Environment()
    result = define.evaluate(env)
    assert result is Null
    assert 123 == env.frames[-1].get(Variable("a")).value

def test_evaluate_with_wrong_params():
    define = Define()
    define.add_child(Variable("a"))
    # with less
    with py.test.raises(SchemeError):
        define.evaluate(Environment())

    define.add_child(Number("123"))
    define.add_child(Number("456"))
    # with too much
    with py.test.raises(SchemeError):
        define.evaluate(Environment())

def test_evaluate_with_complex_value():
    define = Define()
    define.add_child(Variable("a"))

    if_ = If()
    if_.add_child(Variable("b"))
    if_.add_child(Number("1"))
    if_.add_child(Number("0"))
    define.add_child(if_)

    env = Environment()
    env.define(Variable("b"), Bool("#t"))

    define.evaluate(env)
    assert 1 == env.lookup(Variable("a")).value

