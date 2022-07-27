from smallscheme.syntax import *
from smallscheme.runner import *
from smallscheme import SchemeError
import py

def add_block(cond, test, val):
    node = Node()
    node.add_child(test)
    node.add_child(val)
    cond.add_child(node)

def prepare_environment():
    env = Environment()
    env.define(Variable("test-1"), Bool("#f"))
    env.define(Variable("test-2"), Bool("#f"))
    env.define(Variable("second"), Number("2"))
    return env

def test_evaluate():
    cond = Cond()

    if_ = If()
    if_.add_child(Bool("#t"))
    if_.add_child(Number("3"))
    if_.add_child(Number("2"))

    add_block(cond, Variable("test-1"), Number("1"))
    add_block(cond, Variable("test-2"), Variable("second"))
    add_block(cond, Variable("else"), if_)

    env = prepare_environment()

    assert 3 == cond.evaluate(env).value
    env.define(Variable("test-2"), Bool("#t"))
    assert 2 == cond.evaluate(env).value
    env.define(Variable("test-1"), Bool("#t"))
    assert 1 == cond.evaluate(env).value

def test_evaluate_bad():
    cond = Cond()
    node = Node()
    # No childs
    with py.test.raises(SchemeError):
        cond.evaluate(Environment())

    node.add_child(Bool("#t"))
    node.add_child(Number("1"))
    cond.add_child(node)

    # No else statement
    with py.test.raises(SchemeError):
        cond.evaluate(Environment())

def test_evaluate_till_last():
    cond = Cond()

    first = Number(1)
    second = Number(2)
    third = Number(3)

    add_block(cond, Variable("test-1"), first)
    add_block(cond, Variable("test-2"), second)
    add_block(cond, Variable("else"), third)

    env = prepare_environment()

    assert third is cond.evaluate_till_last(env)
    env.define(Variable("test-2"), Bool("#t"))
    assert second is cond.evaluate_till_last(env)
    env.define(Variable("test-1"), Bool("#t"))
    assert first is cond.evaluate_till_last(env)

