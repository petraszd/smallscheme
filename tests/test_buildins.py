from smallscheme import SchemeError
from smallscheme.buildins import *
from smallscheme.runner import Environment
from smallscheme.datatypes import *
from smallscheme.syntax import *
import py

def test_buildins_dict():
    import smallscheme.buildins as b
    required = [
        "car", "cdr", "+", "-", "*", "/", "1+", "1-",
        "zero?", "null?", "=", "<", ">", "<=", ">=",
        "eq?", "display", "newline", "list?", "not",
        "atom?", 'modulo',
    ]
    keys = b.buildins.keys()
    for r in required:
        assert r in keys

class MockOutput(object):
    def __init__(self):
        self.out = []
    def write(self, string):
        self.out.append(string)
    def get(self):
        out = ''.join(self.out)
        self.out = []
        return out

out = MockOutput()
env = Environment(out)

def test_car():
    car = Car(env).call
    assert 1 == car([Pair(Number(1), Number(2))]).value

def test_cdr():
    cdr = Cdr(env).call
    assert 2 == cdr([Pair(Number(1), Number(2))]).value

def test_plus():
    plus = Plus(env).call
    assert 4 == plus([Number(2), Number(2)]).value
    assert 6 == plus([
        Number(1), Number(2), Number(3)
    ]).value
    assert -2 == plus([Number(4), Number(-6)]).value

def test_minus():
    minus = Minus(env).call
    assert 0 == minus([Number(2), Number(2)]).value
    assert -2  == minus([
        Number(2), Number(2), Number(2)
    ]).value
    assert 2 == minus([Number(0), Number(-2)]).value
    assert -1 == minus([Number(1)]).value

def test_multiply():
    multiply = Multiply(env).call
    assert 0 == multiply([Number(4), Number(0)]).value
    assert 4 == multiply([Number(2), Number(2)]).value
    assert -6 == multiply([Number(3), Number(-2)]).value
    assert 27 == multiply([
        Number(3), Number(3), Number(3)
    ]).value

def test_divide():
    divide = Divide(env).call
    assert 2 == divide([Number(4), Number(2)]).value
    assert -3 == divide([Number(9), Number(-3)]).value
    assert 2 == divide([Number(5), Number(2)]).value
    assert -3 == divide([Number(-5), Number(2)]).value
    assert 3 == divide([Number(27), Number(3), Number(3)]).value

    with py.test.raises(SchemeError):
        divide([Number(4), Number(0)])

def test_addone():
    addone = AddOne(env).call
    assert 1 == addone([Number(0)]).value
    assert 2 == addone([Number(1)]).value

def test_minusone():
    minusone = MinusOne(env).call
    assert -1 == minusone([Number(0)]).value
    assert 8 == minusone([Number(9)]).value

def test_iszero():
    iszero = IsZero(env).call
    assert True is iszero([Number(0)]).value
    assert False is iszero([String('""')]).value
    assert False is iszero([Number(1)]).value

def test_isnull():
    isnull = IsNull(env).call
    assert True is isnull([Null]).value
    assert False is isnull([Number(0)]).value
    assert False is isnull([Bool('#t')]).value

def test_numberequal():
    eq = NumberEqual(env).call
    assert True is eq([Number(2), Number(2)]).value
    assert False is eq([Number(1), Number(2)]).value

def test_numberless():
    less = NumberLess(env).call
    assert True is less([Number(1), Number(2)]).value
    assert False is less([Number(1), Number(1)]).value
    assert False is less([Number(2), Number(1)]).value

def test_numbermore():
    more = NumberMore(env).call
    assert False is more([Number(1), Number(2)]).value
    assert False is more([Number(1), Number(1)]).value
    assert True is more([Number(2), Number(1)]).value

def test_numberlessequal():
    lesseq = NumberLessEqual(env).call
    assert True is lesseq([Number(1), Number(2)]).value
    assert True is lesseq([Number(1), Number(1)]).value
    assert False is lesseq([Number(2), Number(1)]).value

def test_numbermoreequal():
    moreeq = NumberMoreEqual(env).call
    assert False is moreeq([Number(1), Number(2)]).value
    assert True is moreeq([Number(1), Number(1)]).value
    assert True is moreeq([Number(2), Number(1)]).value

def test_symbolequal():
    symboleq = SymbolEqual(env).call
    assert True is symboleq([Symbol("'foo"), Symbol("'foo")]).value
    assert False is symboleq([Symbol("'foo"), Symbol("'bar")]).value

def test_display():
    display = Display(env).call
    assert Null is display([Number(1)])
    assert "1" == out.get()

def test_newline():
    newline = Newline(env).call
    assert Null is newline([])
    assert "\n" == out.get()

def test_islist():
    islist = IsList(env).call
    p = Pair(Number(1), Pair(Number(2), Null))
    assert islist([p]).value
    p = Pair(Number(1), Number(2))
    assert not islist([p]).value
    assert not islist([Number(1)]).value
    assert not islist([Bool('#t')]).value
    assert islist([Null]).value

def test_not():
    not_ = Not(env).call
    assert True is not_([Bool('#f')]).value
    assert False is not_([Bool('#t')]).value
    with py.test.raises(SchemeError):
        not_([Number(1)])

def test_isnumber():
    isnumber = IsNumber(env).call
    assert True is isnumber([Number(1)]).value
    assert False is isnumber([Bool('#f')]).value
    assert False is isnumber([String('"123"')]).value
    assert True is isnumber([Symbol("'123")]).value

def test_isatom():
    isatom = IsAtom(env).call
    assert True is isatom([Number(1)]).value
    assert False is isatom([Null]).value
    assert False is isatom([Pair(Number(1), Null)]).value
    assert True is isatom([Bool('#f')]).value

def test_modulo():
    modulo = Modulo(env).call
    assert 0 == modulo([Number(4), Number(2)]).value
    assert 1 == modulo([Number(5), Number(2)]).value

# str
def test_buildin_str():
    assert '<#proc-buildin +>' == str(Plus(env))
    assert '<#proc-buildin list?>' == str(IsList(env))
    class DifferentPlus(Plus): pass
    assert '<#proc-buildin>' == str(DifferentPlus(env))

