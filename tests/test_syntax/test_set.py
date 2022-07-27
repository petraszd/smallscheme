from smallscheme import SchemeError
from smallscheme.datatypes import Null
from smallscheme.syntax import *
from smallscheme.runner import *
import py

def test_evaluate():

    env = Environment()
    env.define(Variable('a'), Number(1))

    set_ = Set()
    set_.add_child(Variable('a'))
    set_.add_child(Number(2))

    env.enter()
    assert set_.evaluate(env) is Null
    assert 2 == env.lookup(Variable('a')).value
    env.exit()

def test_evaluate_bar_params():
    set_ = Set()
    set_.add_child(Variable("b"))
    with py.test.raises(SchemeError):
        set_.evaluate(Environment())
    set_.add_child(Number(1))
    set_.add_child(Number(1))
    with py.test.raises(SchemeError):
        set_.evaluate(Environment())

