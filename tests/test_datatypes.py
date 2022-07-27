from smallscheme.datatypes import *
from smallscheme.syntax import *
from smallscheme.runner import Environment

# Pair
def test_pair_carcdr():
    p = Pair(Number(1), Number(2))
    assert 1 == p.car.value
    assert 2 == p.cdr.value

def test_pair_islist():
    p = Pair(Number(1), Null)
    assert p.islist()
    p = Pair(Number(1), Number(2))
    assert not p.islist()
    p = Pair(Number(1), Pair(Number(2), Null))
    assert p.islist()
    p = Pair(Number(1), Pair(Number(2), Number(3)))
    assert not p.islist()
    p = Pair(Null, Null)
    assert p.islist()
    q = Pair(Number(1), Number(2))
    p = Pair(q, Pair(Number(2), Null))
    assert p.islist()

def test_pair_str():
    assert "(1 . 2)" == str(Pair(Number(1), Number(2)))
    assert "(1 2)" == str(Pair(Number(1), Pair(Number(2), Null)))

# Proc
def test_proc():
    test = Variable("test")
    when_true = Variable("when-true")
    when_false = Variable("when-false")
    scope_works = Variable("scope-works")

    env = Environment()
    env.define(scope_works, Bool("#t"))

    body = ProcBody()

    # to test creation of scope
    define = Define()
    define.add_child(scope_works)
    define.add_child(Bool("#f"))
    body.add_child(define)

    # body with logic
    if_node = If()
    if_node.add_child(test)
    if_node.add_child(when_true)
    if_node.add_child(when_false)
    body.add_child(if_node)

    variables = [test, when_true, when_false]

    # tests if logic works
    proc = Proc(body=body, environment=env, variables=variables)
    args = [Bool("#f"), Number("1"), Number("0")]
    assert 0 == proc.call(args).value
    args = [Bool("#t"), Number("1"), Number("0")]
    proc = Proc(variables, body, env)
    assert 1 == proc.call(args).value

    # tests if scope works
    assert True is env.lookup(scope_works).value

def test_tail_recursion():
    class EnterEnvironment(Environment):
        def __init__(self, *args, **kwargs):
            self.enter_counter = 0
            Environment.__init__(self, *args, **kwargs)
        def enter(self):
            self.enter_counter += 1
            return Environment.enter(self)
    env = EnterEnvironment()

    if_exp = If()
    if_exp.add_child(Variable('quit'))
    if_exp.add_child(Number('1'))

    call = Call()
    call.add_child(Variable('func-name'))
    call.add_child(Bool('#t'))

    if_exp.add_child(call)

    body = ProcBody()
    body.add_child(if_exp)
    variables = [Variable('quit')]
    proc = Proc(variables, body, env)
    env.define(Variable('func-name'), proc)

    result = proc.call([Bool('#f')], name="func-name")
    assert 1 == result.value
    assert 1 == env.enter_counter

def test_proc_str():
    proc = Proc([Variable("x"), Variable("y"), Variable("z")],
                ProcBody(), Environment())
    assert '<#proc (lambda x y z)>' == str(proc)
    proc = Proc([], ProcBody(), Environment())
    assert '<#proc (lambda)>' == str(proc)

# Null
def test_null_str():
    assert "()" == str(Null)

