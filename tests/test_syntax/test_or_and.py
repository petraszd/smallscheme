from smallscheme import SchemeError
from smallscheme.syntax import *
from smallscheme.runner import Environment
import py

class BoolWithState(Bool):
    def __init__(self, *args, **kwargs):
        Bool.__init__(self, *args, **kwargs)
        self.evaluated = False

    def evaluate(self, env):
        self.evaluated = True
        return Bool.evaluate(self, env)

def add_childs(exp, *args):
    result = []
    for arg in args:
        bool_ = BoolWithState(arg)
        exp.add_child(bool_)
        result.append(bool_)
    return result

def test_or_evaluate():
    # False
    or_exp = Or()
    first, second, third = add_childs(or_exp, '#f', '#f', '#f')

    assert not or_exp.evaluate(Environment()).value
    assert first.evaluated
    assert second.evaluated
    assert third.evaluated

    # True
    or_exp = Or()
    first, second, third = add_childs(or_exp, '#f', '#t', '#t')

    assert or_exp.evaluate(Environment()).value
    assert first.evaluated
    assert second.evaluated
    assert not third.evaluated

def test_or_evaluate_bad():
    or_exp = Or()
    or_exp.add_child(Bool('#f'))
    or_exp.add_child(Number(1))
    with py.test.raises(SchemeError):
        or_exp.evaluate(Environment())

def test_and_evaluate():
    # True
    and_exp = And()
    first, second, third = add_childs(and_exp, '#t', '#t', '#t')
    assert and_exp.evaluate(Environment()).value
    assert first.evaluated
    assert second.evaluated
    assert third.evaluated

    # False
    and_exp = And()
    first, second, third = add_childs(and_exp, '#f', '#f', '#f')
    assert not and_exp.evaluate(Environment()).value
    assert first.evaluated
    assert not second.evaluated
    assert not third.evaluated

def test_and_evaluate_bad():
    with py.test.raises(SchemeError):
        and_exp = And()
        and_exp.add_child(Bool('#t'))
        and_exp.add_child(Number(1))
        and_exp.evaluate(Environment())

