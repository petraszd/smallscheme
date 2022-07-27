from smallscheme.datatypes import Proc
from smallscheme.syntax import *
from smallscheme.runner import *

def get_lambda(env):
    lam = Lambda()
    args = Node()
    args.add_child(Variable("arg"))
    lam.add_child(args)
    lam.add_child(Variable("arg"))
    return lam.evaluate(env)

def test_evaluate_with_cons():
    call = Call()
    call.add_child(Variable("func-name"))
    call.add_child(Number("1"))

    env = Environment()
    env.define(Variable("func-name"), get_lambda(env))

    assert 1 == call.evaluate(env).value

def test_evaluate_with_vars():
    call = Call()
    call.add_child(Variable("func-name"))
    call.add_child(Variable("foo"))

    env = Environment()
    env.define(Variable("func-name"), get_lambda(env))
    env.define(Variable("foo"), Number("2"))

    assert 2 == call.evaluate(env).value

def test_evaluate_without_args():
    call = Call()
    call.add_child(Variable("func-name"))

    lam = Lambda()
    args = Node()
    lam.add_child(args)
    lam.add_child(Variable("arg"))

    env = Environment()
    env.define(Variable("func-name"), lam.evaluate(env))
    env.define(Variable("arg"), Number("3"))

    assert 3 == call.evaluate(env).value

def test_get_arguments():
    call = Call()
    call.add_child(Variable("func-name"))
    call.add_child(Number(1))

    env = Environment()
    env.define(Variable("func-name"), get_lambda(env))

    assert 1 == call.get_arguments(env)[0].value

