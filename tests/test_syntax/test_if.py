from smallscheme import SchemeError
from smallscheme.syntax import *
from smallscheme.runner import Environment
import py

def get_if(bool_str):
    if_exp = If()
    if_exp.add_child(Bool(bool_str))
    if_exp.add_child(Number("1"))
    if_exp.add_child(Number("0"))
    return if_exp

def test_evaluate_false():
    env = Environment()
    if_exp = get_if("#f")
    assert 0 == if_exp.evaluate(env).value
    if_exp.childs = if_exp.childs[:-1] # removes else statement
    assert if_exp.evaluate(env).value is False

def test_evaluate_true():
    env = Environment()
    if_exp = get_if("#t")
    if_exp.evaluate(env)
    assert 1 == if_exp.evaluate(env).value

def test_evaluate_not_bool():
    if_exp = get_if("#f")
    if_exp.childs[0] = Number("1")
    with py.test.raises(SchemeError):
        if_exp.evaluate(Environment())

def test_evaluate_till_last():
    env = Environment()

    if_exp = get_if('#t')
    assert if_exp.childs[1] is if_exp.evaluate_till_last(env)

    if_exp = get_if('#f')
    assert if_exp.childs[2] is if_exp.evaluate_till_last(env)
    if_exp.childs = if_exp.childs[:-1]
    assert Bool is type(if_exp.evaluate_till_last(env))

