from smallscheme import runner, parser, SchemeError
from smallscheme.runner import *
from smallscheme.syntax import *
from smallscheme.datatypes import *
from smallscheme.buildins import buildins
import py

# Runner
def test_runner():
    runner = Runner()
    for name in buildins.iterkeys():
        runner.environment.lookup(Variable(name))
    assert Null is runner.run("(define foo 4)")
    assert 4 is runner.run("foo").value

# Frame
def test_frame_define():
    fr = Frame()
    fr.define(Variable("foo"), Number("123"))
    assert 123 == fr.get(Variable("foo")).value

# Environment
def test_environment_enter():
    env = Environment()
    assert 1 == len(env.frames)
    env.enter()
    assert 2 == len(env.frames)

def test_environment_exit():
    env = Environment()
    env.enter()
    env.enter()
    env.exit()
    assert 2 == len(env.frames)

def test_environment_lookup():
    env = Environment()
    foo = Variable("foo")

    env.define(foo, Number("123"))
    assert 123 == env.lookup(foo).value

    env.enter()
    assert 123 == env.lookup(foo).value

    env.define(foo, Number("456"))
    assert 456 == env.lookup(foo).value

    env.exit()
    assert 123 == env.lookup(foo).value

    with py.test.raises(SchemeError):
        env.lookup(Variable("non-exist"))

def test_environment_set():
    foo = Variable("foo")
    env = Environment() # <----- frame[0]

    env.enter() # <------------- frame[1]
    env.define(foo, Number("123"))
    env.set(foo, Number("456"))
    assert 456 == env.lookup(foo).value
    env.enter() # <------------- frame[2]
    env.set(foo, Number("789"))
    assert 789 == env.lookup(foo).value
    env.exit() # <-------------- frame[1]
    assert 789 == env.lookup(foo).value
    env.exit() # <-------------- frame[0]

    with py.test.raises(SchemeError):
        # sets undefined variable
        env.set(foo, Number("000"))

def test_environment_output_buffer():
    class OutputMock(object):
        def __init__(self):
            self.out = ""
        def write(self, string):
            self.out += string

    out = OutputMock()
    env = Environment(out)
    env.write("foo")
    env.write("-")
    env.write("bar")
    assert "foo-bar" == out.out

def test_environment_copy():
    env = Environment()
    env.enter()
    env.define(Variable("foo"), Number(1))
    env_copy = env.copy()
    env.exit()

    # must have
    env_copy.lookup(Variable("foo"))

    with py.test.raises(SchemeError):
        env.lookup(Variable("foo"))


