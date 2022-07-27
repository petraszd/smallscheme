from smallscheme import SchemeError
from smallscheme.syntax import *
from smallscheme.runner import *
import py

def test_evaluate_till_last():
    env = Environment()
    procbody = ProcBody()
    with py.test.raises(SchemeError):
        procbody.evaluate_till_last(env)
    procbody.add_child(Number(1))
    procbody.add_child(Number(2))
    last = Number(3)
    procbody.add_child(last)
    assert last is procbody.evaluate_till_last(env)

    class Mock(object):
        def evaluate_till_last(self, env):
            return "it works"

    procbody.add_child(Mock())
    assert "it works" == procbody.evaluate_till_last(env)

