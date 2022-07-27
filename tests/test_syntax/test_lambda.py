from smallscheme.datatypes import Proc
from smallscheme.syntax import *
from smallscheme.runner import *

def test_evaluate():
    lam = Lambda()
    args = Node()
    args.add_child(Variable("foo"))
    lam.add_child(args)
    lam.add_child(Number(2))
    lam.add_child(Variable("foo"))

    env = Environment()
    result = lam.evaluate(env)
    assert Proc == type(result)
    assert 1 == result.call([Number("1")]).value

    # Proc.environment must be a copy
    assert not env is result.environment

